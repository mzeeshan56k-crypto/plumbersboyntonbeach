#!/usr/bin/env python3
"""Publish one weekly batch of blog posts.

Posts for weeks 2-5 live on the `content-queue` branch under queue/<slug>/,
which Vercel never deploys because it only builds `main`. This script moves
one week's batch onto the current branch, rebuilds the blog index and
sitemap, then commits and pushes.

Usage:  python3 scripts/publish_batch.py <week-number>
"""
import json, os, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run(*a, **kw):
    return subprocess.run(a, cwd=ROOT, check=True, text=True,
                          capture_output=kw.get('cap', False))

def main():
    if len(sys.argv) != 2:
        sys.exit('usage: publish_batch.py <week-number>')
    week = int(sys.argv[1])
    sched = json.load(open(os.path.join(ROOT, 'scripts', 'blog_schedule.json')))
    slugs = sorted(s for s, v in sched.items() if v['week'] == week)
    if not slugs:
        sys.exit(f'no posts scheduled for week {week}')

    run('git', 'fetch', 'origin', 'content-queue')
    published = []
    for slug in slugs:
        dest = os.path.join(ROOT, 'blog', slug)
        if os.path.exists(dest):
            print(f'  already published: {slug}')
            continue
        run('git', 'checkout', 'origin/content-queue', '--', f'queue/{slug}')
        shutil.move(os.path.join(ROOT, 'queue', slug), dest)
        published.append(slug)
    qdir = os.path.join(ROOT, 'queue')
    if os.path.isdir(qdir) and not os.listdir(qdir):
        os.rmdir(qdir)
    run('git', 'reset')

    if not published:
        print('nothing new to publish')
        return
    subprocess.run([sys.executable, os.path.join(ROOT, 'scripts', 'rebuild_blog.py')],
                   cwd=ROOT, check=True)
    run('git', 'add', '-A')
    msg = (f'Publish blog week {week}: {len(published)} posts\n\n' +
           '\n'.join('  ' + s for s in published) +
           '\n\nBlog index and sitemap rebuilt from the published set.\n')
    subprocess.run(['git', '-c', 'user.name=Claude',
                    '-c', 'user.email=noreply@anthropic.com',
                    'commit', '-q', '-m', msg], cwd=ROOT, check=True)
    print(f'committed {len(published)} posts for week {week}')

if __name__ == '__main__':
    main()
