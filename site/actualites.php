<?php
require __DIR__ . '/inc/bootstrap.php';
$rows = db()->query("SELECT slug, title, category, description, cover, published_at FROM pc_articles WHERE status = 'published' AND published_at <= UTC_DATE() ORDER BY published_at DESC, id DESC LIMIT 200")->fetchAll();
$html = '';
foreach ($rows as $r) {
  $th = $r['cover'] ? '<img class="th" src="uploads/' . e($r['cover']) . '" alt="" width="200" height="112" loading="lazy">' : '';
  $html .= '<a class="cd ar" href="actualites/' . e($r['slug']) . '.html">' . $th . '<span class="mt">' . e(fdate_fr($r['published_at'])) . ' · ' . e($r['category']) . '</span><h3>' . e($r['title']) . '</h3><p>' . e($r['description']) . '</p></a>';
}
if ($html === '') $html = '<p>Aucun article pour le moment.</p>';
$tpl = (string)file_get_contents(__DIR__ . '/tpl/actualites.html');
$out = preg_replace_callback('~<!--LIST-->.*?<!--/LIST-->~s', function () use ($html) { return $html; }, $tpl, 1);
header('Content-Type: text/html; charset=utf-8');
header('Cache-Control: public, max-age=120');
echo $out;
