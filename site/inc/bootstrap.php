<?php
// Perfect Conseil – noyau commun (compatible PHP 7.4+)
error_reporting(E_ALL);
ini_set('display_errors', '0');
ini_set('log_errors', '1');
define('PC_ROOT', dirname(__DIR__));
$GLOBALS['PC_CFG'] = is_file(__DIR__ . '/config.php') ? (require __DIR__ . '/config.php') : array();

function cfg($k, $d = null) { return isset($GLOBALS['PC_CFG'][$k]) ? $GLOBALS['PC_CFG'][$k] : $d; }
function e($s) { return htmlspecialchars((string)$s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8'); }
function is_https() { return (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') || (isset($_SERVER['HTTP_X_FORWARDED_PROTO']) && $_SERVER['HTTP_X_FORWARDED_PROTO'] === 'https'); }
function fail($code, $msg) { http_response_code($code); header('Content-Type: text/plain; charset=utf-8'); header('Cache-Control: no-store'); echo $msg; exit; }
function client_ip() { return isset($_SERVER['REMOTE_ADDR']) ? substr((string)$_SERVER['REMOTE_ADDR'], 0, 45) : '0.0.0.0'; }

set_exception_handler(function ($ex) { error_log('PC fatal: ' . $ex->getMessage()); fail(500, 'Erreur interne. / خطأ داخلي.'); });

function db() {
  static $pdo = null;
  if ($pdo === null) {
    $c = cfg('db');
    if (!$c) fail(503, 'Site non installé.');
    try {
      $pdo = new PDO('mysql:host=' . $c['host'] . ';dbname=' . $c['name'] . ';charset=utf8mb4', $c['user'], $c['pass'], array(
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        PDO::ATTR_EMULATE_PREPARES => false,
      ));
      $pdo->exec("SET time_zone = '+00:00'");
    } catch (PDOException $ex) { error_log('PC db: ' . $ex->getMessage()); fail(503, 'Service temporairement indisponible.'); }
  }
  return $pdo;
}

/* ---------- sessions & CSRF ---------- */
function start_session() {
  if (session_status() === PHP_SESSION_ACTIVE) return;
  ini_set('session.use_strict_mode', '1');
  ini_set('session.use_only_cookies', '1');
  ini_set('session.cookie_httponly', '1');
  session_name('pc_admin');
  session_set_cookie_params(0, '/', '', is_https(), true);
  if (PHP_VERSION_ID >= 70300) session_set_cookie_params(array('lifetime' => 0, 'path' => '/', 'secure' => is_https(), 'httponly' => true, 'samesite' => 'Strict'));
  session_start();
  $now = time();
  if (isset($_SESSION['last']) && ($now - $_SESSION['last']) > 7200) { $_SESSION = array(); session_regenerate_id(true); }
  $_SESSION['last'] = $now;
}
function csrf_token() { start_session(); if (empty($_SESSION['csrf'])) $_SESSION['csrf'] = bin2hex(random_bytes(32)); return $_SESSION['csrf']; }
function csrf_field() { return '<input type="hidden" name="csrf" value="' . e(csrf_token()) . '">'; }
function csrf_check() {
  start_session();
  $t = isset($_POST['csrf']) ? $_POST['csrf'] : '';
  if (!is_string($t) || empty($_SESSION['csrf']) || !hash_equals($_SESSION['csrf'], $t)) fail(400, 'طلب غير صالح (CSRF).');
}
function current_user() {
  start_session();
  if (empty($_SESSION['uid'])) return null;
  $st = db()->prepare('SELECT id, email FROM pc_users WHERE id = ?');
  $st->execute(array((int)$_SESSION['uid']));
  $u = $st->fetch();
  return $u ? $u : null;
}
function require_login() {
  $u = current_user();
  if (!$u) { header('Location: login.php'); exit; }
  return $u;
}
function admin_headers() {
  header('Content-Type: text/html; charset=utf-8');
  header('Cache-Control: no-store, no-cache, must-revalidate');
  header('Pragma: no-cache');
  header("Content-Security-Policy: default-src 'none'; script-src 'self'; style-src 'self'; img-src 'self' data: blob:; connect-src 'self'; form-action 'self'; base-uri 'none'; frame-ancestors 'none'");
  header('X-Frame-Options: DENY');
  header('X-Content-Type-Options: nosniff');
  header('Referrer-Policy: no-referrer');
  header('X-Robots-Tag: noindex, nofollow');
}

/* ---------- limitation des tentatives de connexion ---------- */
function login_blocked($ip, $email) {
  $st = db()->prepare('SELECT COUNT(*) FROM pc_login_attempts WHERE attempted_at > (UTC_TIMESTAMP() - INTERVAL 15 MINUTE) AND (ip = ? OR (email <> "" AND email = ?))');
  $st->execute(array($ip, $email));
  return (int)$st->fetchColumn() >= 6;
}
function login_failed($ip, $email) {
  db()->prepare('INSERT INTO pc_login_attempts (ip, email, attempted_at) VALUES (?, ?, UTC_TIMESTAMP())')->execute(array($ip, substr($email, 0, 190)));
  db()->exec('DELETE FROM pc_login_attempts WHERE attempted_at < (UTC_TIMESTAMP() - INTERVAL 2 DAY)');
}
function login_cleared($ip, $email) { db()->prepare('DELETE FROM pc_login_attempts WHERE ip = ? OR email = ?')->execute(array($ip, $email)); }

/* ---------- texte ---------- */
function slugify($s) {
  $s = mb_strtolower((string)$s, 'UTF-8');
  $s = strtr($s, array('à'=>'a','â'=>'a','ä'=>'a','á'=>'a','ç'=>'c','é'=>'e','è'=>'e','ê'=>'e','ë'=>'e','î'=>'i','ï'=>'i','í'=>'i','ô'=>'o','ö'=>'o','ó'=>'o','ù'=>'u','û'=>'u','ü'=>'u','ú'=>'u','ÿ'=>'y','œ'=>'oe','æ'=>'ae','ñ'=>'n'));
  $s = preg_replace('~[^a-z0-9]+~', '-', $s);
  return substr(trim($s, '-'), 0, 90);
}
function valid_slug($s) { return (bool)preg_match('~^[a-z0-9]+(-[a-z0-9]+)*$~', $s) && strlen($s) <= 100; }
function fdate_fr($d) {
  $m = array('janvier','février','mars','avril','mai','juin','juillet','août','septembre','octobre','novembre','décembre');
  $p = explode('-', substr((string)$d, 0, 10));
  return (count($p) === 3 && isset($m[(int)$p[1] - 1])) ? ((int)$p[2] . ' ' . $m[(int)$p[1] - 1] . ' ' . $p[0]) : (string)$d;
}
function valid_date($d) { $x = DateTime::createFromFormat('Y-m-d', (string)$d); return $x && $x->format('Y-m-d') === $d; }

/* ---------- nettoyage strict du HTML des articles (liste blanche) ---------- */
function san_children($n) {
  static $ok = array('p','h2','h3','strong','em','ul','ol','li','blockquote','br','a');
  static $dir = array('p','h2','h3','li','blockquote');
  $o = '';
  foreach ($n->childNodes as $c) {
    if ($c->nodeType === XML_TEXT_NODE) { $o .= e($c->nodeValue); continue; }
    if ($c->nodeType !== XML_ELEMENT_NODE) continue;
    $t = strtolower($c->nodeName);
    if ($t === 'script' || $t === 'style' || $t === 'iframe' || $t === 'object' || $t === 'embed' || $t === 'template' || $t === 'noscript') continue;
    if ($t === 'b') $t = 'strong'; elseif ($t === 'i') $t = 'em'; elseif ($t === 'div') $t = 'p';
    elseif ($t === 'h1' || $t === 'h4' || $t === 'h5' || $t === 'h6') $t = 'h2';
    if (!in_array($t, $ok, true)) { $o .= san_children($c); continue; }
    if ($t === 'br') { $o .= '<br>'; continue; }
    if ($t === 'a') {
      $h = trim($c->getAttribute('href'));
      if (!preg_match('~^(https?://|mailto:)~i', $h)) { $o .= san_children($c); continue; }
      $o .= '<a href="' . e($h) . '" rel="noopener noreferrer">' . san_children($c) . '</a>'; continue;
    }
    $o .= '<' . $t . (in_array($t, $dir, true) ? ' dir="auto"' : '') . '>' . san_children($c) . '</' . $t . '>';
  }
  return $o;
}
function sanitize_html($html) {
  $html = (string)$html;
  if (trim($html) === '') return '';
  $d = new DOMDocument();
  libxml_use_internal_errors(true);
  $d->loadHTML('<?xml encoding="UTF-8"><html><body>' . $html . '</body></html>', LIBXML_HTML_NODEFDTD);
  libxml_clear_errors();
  $b = $d->getElementsByTagName('body')->item(0);
  $s = $b ? san_children($b) : '';
  $s = preg_replace('~<(p|h2|h3|li|blockquote|strong|em)( dir="auto")?>(\s|<br>|\xC2\xA0)*</\1>~u', '', $s);
  $s = preg_replace('~^(?!<)([^<]+)~u', '<p dir="auto">$1</p>', $s);
  return trim((string)$s);
}
function plain_len($html) { return mb_strlen(trim(preg_replace('~\s+~u', ' ', strip_tags((string)$html))), 'UTF-8'); }

/* ---------- image de couverture (GD ou Imagick), recadrée 1200x675 et ré-encodée ---------- */
function save_cover($f, &$err) {
  if (!is_array($f) || !isset($f['error']) || $f['error'] === UPLOAD_ERR_NO_FILE) return null;
  if ($f['error'] !== UPLOAD_ERR_OK || $f['size'] > 8 * 1024 * 1024 || !is_uploaded_file($f['tmp_name'])) { $err = 'تعذّر رفع الصورة (الحد الأقصى 8 ميغابايت).'; return null; }
  $info = @getimagesize($f['tmp_name']);
  if (!$info || !in_array($info[2], array(IMAGETYPE_JPEG, IMAGETYPE_PNG, IMAGETYPE_WEBP), true) || $info[0] * $info[1] > 40000000) { $err = 'صيغة الصورة غير مقبولة (JPG أو PNG أو WebP فقط).'; return null; }
  $dir = PC_ROOT . '/uploads';
  if (!is_dir($dir)) @mkdir($dir, 0755, true);
  $W = 1200; $H = 675; $base = bin2hex(random_bytes(10));
  if (function_exists('imagecreatefromstring') && function_exists('imagecopyresampled')) {
    $src = @imagecreatefromstring((string)file_get_contents($f['tmp_name']));
    if ($src) {
      $sw = imagesx($src); $sh = imagesy($src); $r = max($W / $sw, $H / $sh);
      $cw = (int)round($W / $r); $ch = (int)round($H / $r);
      $dst = imagecreatetruecolor($W, $H);
      imagecopyresampled($dst, $src, 0, 0, (int)(($sw - $cw) / 2), (int)(($sh - $ch) / 2), $W, $H, $cw, $ch);
      if (function_exists('imagewebp')) { $name = $base . '.webp'; $ok = @imagewebp($dst, $dir . '/' . $name, 82); }
      else { $name = $base . '.jpg'; $ok = @imagejpeg($dst, $dir . '/' . $name, 84); }
      if ($ok) { @chmod($dir . '/' . $name, 0644); return $name; }
    }
  }
  if (class_exists('Imagick')) {
    try {
      $im = new Imagick($f['tmp_name']); $im->setIteratorIndex(0); $im->stripImage();
      $im->cropThumbnailImage($W, $H); $im->setImageFormat('jpeg'); $im->setImageCompressionQuality(84);
      $name = $base . '.jpg'; $im->writeImage($dir . '/' . $name); $im->clear(); @chmod($dir . '/' . $name, 0644); return $name;
    } catch (Exception $ex) { error_log('PC imagick: ' . $ex->getMessage()); }
  }
  $err = 'تعذّرت معالجة الصورة على الخادم.';
  return null;
}
function delete_cover($name) { if ($name && preg_match('~^[a-f0-9]{20}\.(webp|jpg)$~', $name)) @unlink(PC_ROOT . '/uploads/' . $name); }

function hash_pw($p) { return password_hash($p, PASSWORD_BCRYPT, array('cost' => 12)); }
function pw_ok_policy($p) { return strlen($p) >= 12 && strlen($p) <= 200; }
