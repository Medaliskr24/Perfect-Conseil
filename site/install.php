<?php
// Installateur unique. Il se supprime automatiquement après une installation réussie.
require __DIR__ . '/inc/bootstrap.php';
header('Content-Type: text/html; charset=utf-8');
header('Cache-Control: no-store');
header("Content-Security-Policy: default-src 'none'; style-src 'unsafe-inline'; form-action 'self'; base-uri 'none'; frame-ancestors 'none'");
header('X-Robots-Tag: noindex, nofollow');
$cfgFile = __DIR__ . '/inc/config.php';
function page_out($title, $inner) {
  echo '<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>' . e($title) . '</title><style>body{font:16px/1.6 system-ui,"Segoe UI",Tahoma,sans-serif;background:linear-gradient(135deg,#14233f,#2977b9 60%,#7a52a6);min-height:100vh;margin:0;display:grid;place-items:center;padding:20px}.c{background:#fff;border-radius:22px;padding:30px;max-width:560px;width:100%;box-shadow:0 30px 80px rgba(0,0,0,.35)}h1{margin-top:0;font-size:1.4rem}label{display:block;font-weight:600;margin:12px 0 4px;font-size:.92rem}input[type=text],input[type=email],input[type=password],input[type=url]{width:100%;padding:11px 12px;border:1px solid #cfdbe7;border-radius:10px;font:inherit;direction:ltr}button{margin-top:18px;width:100%;padding:13px;border:0;border-radius:12px;background:linear-gradient(120deg,#41a0de,#2977b9 50%,#7a52a6);color:#fff;font:700 1rem inherit;cursor:pointer}.e{background:#fdeaea;color:#b3261e;border-radius:10px;padding:10px 14px;margin:10px 0}.o{background:#e3f6ea;color:#17803d;border-radius:10px;padding:10px 14px}.h{color:#64748b;font-size:.85rem}.k{display:flex;gap:8px;align-items:center;font-weight:400}a{color:#2977b9}</style></head><body><div class="c">' . $inner . '</div></body></html>';
  exit;
}
if (is_file($cfgFile)) page_out('مثبّت مسبقاً', '<h1>الموقع مثبّت مسبقاً</h1><p>احذف الملف <b dir="ltr">install.php</b> من الخادم، ثم ادخل إلى <a href="admin/login.php">لوحة التحكم</a>.</p>');
if (!extension_loaded('pdo_mysql')) page_out('خطأ', '<div class="e">امتداد PDO MySQL غير مفعّل على الخادم.</div>');
start_session();
$errs = array();
$v = array('host' => 'localhost', 'name' => 'perfect-conseil.com_main', 'user' => 'perfect-conseil.com_main', 'url' => (is_https() ? 'https://' : 'http://') . (isset($_SERVER['HTTP_HOST']) ? preg_replace('~[^a-z0-9.\-:]~i', '', $_SERVER['HTTP_HOST']) : 'www.perfect-conseil.com'), 'email' => '');
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
  csrf_check();
  foreach (array('host', 'name', 'user', 'url', 'email') as $k) $v[$k] = trim((string)(isset($_POST[$k]) ? $_POST[$k] : ''));
  $dbpass = (string)(isset($_POST['dbpass']) ? $_POST['dbpass'] : '');
  $p1 = (string)(isset($_POST['p1']) ? $_POST['p1'] : ''); $p2 = (string)(isset($_POST['p2']) ? $_POST['p2'] : '');
  $v['email'] = strtolower($v['email']);
  if (!filter_var($v['email'], FILTER_VALIDATE_EMAIL)) $errs[] = 'البريد الإلكتروني للمسؤول غير صالح.';
  if (!pw_ok_policy($p1) || $p1 !== $p2) $errs[] = 'كلمة سر المسؤول: 12 حرفاً على الأقل ومتطابقة في الخانتين.';
  if (!preg_match('~^https?://[a-z0-9.\-]+(:\d+)?(/[^\s]*)?$~i', $v['url'])) $errs[] = 'عنوان الموقع غير صالح.';
  if (!preg_match('~^[A-Za-z0-9._-]{1,100}$~', $v['host']) || !preg_match('~^[A-Za-z0-9._$-]{1,64}$~', $v['name']) || !preg_match('~^[A-Za-z0-9._@$-]{1,80}$~', $v['user'])) $errs[] = 'خادم أو اسم أو مستخدم قاعدة البيانات يحتوي على أحرف غير مقبولة.';
  if (!$errs) {
    try {
      $pdo = new PDO('mysql:host=' . $v['host'] . ';dbname=' . $v['name'] . ';charset=utf8mb4', $v['user'], $dbpass, array(PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION));
      foreach (array_filter(array_map('trim', explode(';', (string)file_get_contents(__DIR__ . '/inc/schema.sql')))) as $sql) $pdo->exec($sql);
      if ((int)$pdo->query('SELECT COUNT(*) FROM pc_users')->fetchColumn() > 0) throw new Exception('exists');
      $pdo->prepare('INSERT INTO pc_users (email, password_hash, created_at) VALUES (?, ?, UTC_TIMESTAMP())')->execute(array($v['email'], hash_pw($p1)));
      if (!empty($_POST['seed']) && is_file(__DIR__ . '/inc/seed.json')) {
        $seed = json_decode((string)file_get_contents(__DIR__ . '/inc/seed.json'), true);
        $ins = $pdo->prepare('INSERT IGNORE INTO pc_articles (slug, title, category, description, body, cover, status, published_at, created_at, updated_at) VALUES (?,?,?,?,?,NULL,"published",?,UTC_TIMESTAMP(),UTC_TIMESTAMP())');
        if (is_array($seed)) foreach ($seed as $a) $ins->execute(array($a['slug'], $a['title'], $a['cat'], $a['desc'], sanitize_html($a['html']), $a['date']));
      }
      $cfg = array('db' => array('host' => $v['host'], 'name' => $v['name'], 'user' => $v['user'], 'pass' => $dbpass), 'site_url' => rtrim($v['url'], '/'), 'installed_at' => gmdate('c'));
      if (file_put_contents($cfgFile, "<?php\nreturn " . var_export($cfg, true) . ";\n", LOCK_EX) === false) throw new Exception('write');
      @chmod($cfgFile, 0640);
      if (!is_dir(PC_ROOT . '/uploads')) @mkdir(PC_ROOT . '/uploads', 0755, true);
      $del = @unlink(__FILE__);
      page_out('تم التثبيت', '<h1>تم التثبيت بنجاح ✔</h1><div class="o">تم إنشاء الجداول وحساب المسؤول.</div>' . ($del ? '<p>تم حذف ملف التثبيت تلقائياً.</p>' : '<div class="e">لم أستطع حذف <b dir="ltr">install.php</b>. احذفه الآن يدوياً من الخادم!</div>') . '<p><a href="admin/login.php">الدخول إلى لوحة التحكم ←</a></p>');
    } catch (PDOException $ex) { error_log('PC install: ' . $ex->getMessage()); $errs[] = 'تعذّر الاتصال بقاعدة البيانات أو إنشاء الجداول. تحقّق من الاسم والمستخدم وكلمة السر.'; }
    catch (Exception $ex) { $errs[] = $ex->getMessage() === 'exists' ? 'توجد حسابات في قاعدة البيانات مسبقاً. استعمل قاعدة بيانات فارغة.' : 'تعذّر كتابة ملف الإعداد inc/config.php (تحقّق من صلاحيات المجلد).'; }
  }
}
$f = function ($n, $t, $val, $extra = '') { return '<label for="' . $n . '">' . $t . '</label><input id="' . $n . '" name="' . $n . '" type="' . ($n === 'email' ? 'email' : ($n === 'url' ? 'url' : 'text')) . '" value="' . e($val) . '" ' . $extra . ' required>'; };
$err = $errs ? '<div class="e"><ul style="margin:0;padding-inline-start:18px">' . implode('', array_map(function ($x) { return '<li>' . e($x) . '</li>'; }, $errs)) . '</ul></div>' : '';
page_out('تثبيت Perfect Conseil', '<h1>تثبيت لوحة المقالات</h1><p class="h">استعمل قاعدة بيانات <b>جديدة وفارغة</b> ومستخدماً جديداً بكلمة سر قوية (أنشئها من لوحة الاستضافة أو phpMyAdmin). لا تعيد استعمال بيانات موقع WordPress القديم.</p>' . $err . '<form method="post" autocomplete="off">' . csrf_field()
  . $f('host', 'خادم قاعدة البيانات', $v['host']) . $f('name', 'اسم قاعدة البيانات', $v['name']) . $f('user', 'مستخدم قاعدة البيانات', $v['user'])
  . '<label for="dbpass">كلمة سر قاعدة البيانات</label><input id="dbpass" name="dbpass" type="password" autocomplete="off">'
  . $f('url', 'عنوان الموقع', $v['url']) . '<hr style="border:0;border-top:1px solid #e3ebf3;margin:18px 0">'
  . $f('email', 'بريد المسؤول (لتسجيل الدخول)', $v['email'], 'autocomplete="off"')
  . '<label for="p1">كلمة سر المسؤول (12 حرفاً على الأقل)</label><input id="p1" name="p1" type="password" autocomplete="new-password" minlength="12" required>'
  . '<label for="p2">تأكيد كلمة السر</label><input id="p2" name="p2" type="password" autocomplete="new-password" minlength="12" required>'
  . '<label class="k"><input type="checkbox" name="seed" value="1" checked> إضافة المقالين التجريبيين الحاليين</label><button type="submit">تثبيت</button></form>');
