<?php
require __DIR__ . '/inc/bootstrap.php';
$slug = isset($_GET['slug']) ? (string)$_GET['slug'] : '';
if (!valid_slug($slug)) fail(404, 'Not found');
$st = db()->prepare("SELECT * FROM pc_articles WHERE slug = ? AND status = 'published' AND published_at <= UTC_DATE() LIMIT 1");
$st->execute(array($slug));
$a = $st->fetch();
if (!$a) {
  http_response_code(404); header('Content-Type: text/html; charset=utf-8');
  echo '<!DOCTYPE html><html lang="fr"><meta charset="utf-8"><meta name="robots" content="noindex"><title>Article introuvable</title><body style="font-family:system-ui;text-align:center;padding:60px"><h1>Article introuvable</h1><p><a href="../actualites.html">Retour aux actualités</a></p>';
  exit;
}
$tpl = (string)file_get_contents(__DIR__ . '/tpl/article.html');
$cover = $a['cover'] ? '<figure class="cv"><img src="../uploads/' . e($a['cover']) . '" alt="' . e($a['title']) . '" width="1200" height="675"></figure>' : '';
$base = rtrim((string)cfg('site_url', ''), '/');
$ld = json_encode(array('@context' => 'https://schema.org', '@type' => 'Article', 'headline' => $a['title'], 'description' => $a['description'], 'datePublished' => $a['published_at'], 'dateModified' => substr($a['updated_at'], 0, 10), 'author' => array('@type' => 'Organization', 'name' => 'Perfect Conseil'), 'mainEntityOfPage' => $base . '/actualites/' . $a['slug'] . '.html'), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_HEX_TAG);
$out = strtr($tpl, array(
  '§J§' => $ld, '§T§' => e($a['title']), '§D§' => e($a['description']), '§DATE§' => fdate_fr($a['published_at']),
  '§C§' => e($a['category']), '__tpl' => $a['slug'], '§IMG§' => $cover, '§B§' => $a['body'],
));
header('Content-Type: text/html; charset=utf-8');
header('Cache-Control: public, max-age=300');
header('Last-Modified: ' . gmdate('D, d M Y H:i:s', strtotime($a['updated_at'] . ' UTC')) . ' GMT');
echo $out;
