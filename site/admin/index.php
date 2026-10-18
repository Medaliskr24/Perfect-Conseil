<?php
require __DIR__ . '/../inc/bootstrap.php';
require __DIR__ . '/_ui.php';
$u = require_login();
$s = db()->query("SELECT COUNT(*) t, SUM(status='published') p, SUM(status='draft') d FROM pc_articles")->fetch();
$rows = db()->query('SELECT id, slug, title, category, status, published_at, cover FROM pc_articles ORDER BY published_at DESC, id DESC LIMIT 500')->fetchAll();
ui_head('المقالات', 'ad');
echo '<div class="app">'; ui_side($u, 'list'); echo '<main>' . ui_flash();
echo '<div class="stats"><div class="st"><b>' . (int)$s['t'] . '</b><span>إجمالي المقالات</span></div><div class="st g"><b>' . (int)$s['p'] . '</b><span>منشورة</span></div><div class="st y"><b>' . (int)$s['d'] . '</b><span>مسودات</span></div></div>';
echo '<div class="cd"><div class="hd"><h1>المقالات</h1><div class="hd2"><input id="q" type="search" placeholder="ابحث في العناوين…" dir="auto"><a class="b p" href="edit.php">+ مقال جديد</a></div></div>';
if (!$rows) { echo '<p class="hint">لا توجد مقالات بعد. اضغط «مقال جديد» للبدء.</p>'; }
else {
  echo '<div class="tw"><table><thead><tr><th>العنوان</th><th>الفئة</th><th>التاريخ</th><th>الحالة</th><th></th></tr></thead><tbody>';
  foreach ($rows as $r) {
    $sched = $r['status'] === 'published' && $r['published_at'] > gmdate('Y-m-d');
    $stl = $r['status'] === 'draft' ? '<span class="tg y">مسودة</span>' : ($sched ? '<span class="tg b">مجدول</span>' : '<span class="tg g">منشور</span>');
    echo '<tr data-t="' . e(mb_strtolower($r['title'], 'UTF-8')) . '"><td dir="auto"><a href="edit.php?id=' . (int)$r['id'] . '"><b>' . e($r['title']) . '</b></a></td><td dir="auto">' . e($r['category']) . '</td><td>' . e($r['published_at']) . '</td><td>' . $stl . '</td><td class="ac2"><a href="edit.php?id=' . (int)$r['id'] . '">تعديل</a>'
      . ($r['status'] === 'published' && !$sched ? ' · <a href="../actualites/' . e($r['slug']) . '.html" target="_blank" rel="noopener">عرض ↗</a>' : '') . '</td></tr>';
  }
  echo '</tbody></table></div>';
}
echo '</div></main></div>';
ui_end();
