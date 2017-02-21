#!/usr/bin/python
# encoding: utf-8
from __future__ import unicode_literals

import sys
import argparse

from workflow.workflow import Workflow, ICON_WARNING
from os import listdir


def list_dirs(path):
    from os.path import isdir, join

    return [f for f in listdir(path) if isdir(join(path, f))]


def is_intellij_project(path, d):
    project_files = [f for f in listdir(path + '/' + d) if f.endswith('.iml') or f == '.idea' or f == 'pom.xml' or f == 'build.gradle']

    return len(project_files)


def filter_intellij_projects(path):
    intellij_dirs = [d for d in list_dirs(path) if is_intellij_project(path, d)]
    return intellij_dirs


def set_projects_path(wf, args):
    wf.settings['projects_path'] = args.projects_path
    return 0


def ask_for_project_path(wf):
    wf.add_item('No IntelliJ project path set.',
                'Please use ijpath to set your IntelliJ projects path.',
                valid=False,
                icon=ICON_WARNING)
    wf.send_feedback()
    return 0


def filter_on_query(query, names):
    if query:
        return [name for name in names if name.lower().startswith(query.lower())]
    else:
        return names


def add_project_items(filtered_intellij_projects, projects_path, wf):
    for intellij_dir in filtered_intellij_projects:
        wf.add_item(title=intellij_dir,
                    arg=projects_path + '/' + intellij_dir,
                    subtitle=projects_path + '/' + intellij_dir,
                    valid=True)


def list_intellij_projects(args, projects_path, wf):
    filtered_intellij_projects = filter_on_query(args.query, filter_intellij_projects(projects_path))
    if not filtered_intellij_projects:
        wf.add_item('No project found', icon=ICON_WARNING)
    else:
        add_project_items(filtered_intellij_projects, projects_path, wf)

    wf.send_feedback()
    return 0


def main(wf):
    parser = argparse.ArgumentParser()
    parser.add_argument('--set_projects_path', dest='projects_path', nargs='?', default=None)
    parser.add_argument('query', nargs='?', default=None)

    args = parser.parse_args(wf.args)

    if args.projects_path:  # Script was passed a new project path
        return set_projects_path(wf, args)

    projects_path = wf.settings.get('projects_path', None)
    if not projects_path:  # project path has not yet been set
        return ask_for_project_path(wf)

    return list_intellij_projects(args, projects_path, wf)


if __name__ == u"__main__":
    sys.exit(Workflow().run(main))
