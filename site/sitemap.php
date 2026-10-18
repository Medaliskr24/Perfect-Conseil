<?php
require __DIR__ . '/inc/bootstrap.php';
$base = rtrim((string)cfg('site_url', ''), '/');
$pages = json_decode((string)@file_get_contents(__DIR__ . '/inc/static_pages.json'), true);
if (!is_array($pages)) $pages = array('index.html');
$x = '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">';
foreach ($pages as $p) { $x .= '<url><loc>' . e($base . '/' . ($p === 'index.html' ? '' : $p)) . '</loc></url>'; }
$st = db()->query("SELECT slug, published_at, updated_at FROM pc_articles WHERE status = 'published' AND published_at <= UTC_DATE() ORDER BY published_at DESC");
foreach ($st as $r) { $x .= '<url><loc>' . e($base . '/actualites/' . $r['slug'] . '.html') . '</loc><lastmod>' . e(substr($r['updated_at'], 0, 10)) . '</lastmod></url>'; }
header('Content-Type: application/xml; charset=utf-8');
header('Cache-Control: public, max-age=3600');
echo $x . '</urlset>';
