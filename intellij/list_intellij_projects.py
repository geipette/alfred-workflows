#!/usr/bin/python
# encoding: utf-8

import sys

from workflow.workflow import Workflow, Item
from os import listdir


def list_dirs(path):
    from os.path import isdir, join

    return [f for f in listdir(path) if isdir(join(path, f))]


def is_intellij_project(path, d):
    project_files = [f for f in listdir(path + '/' + d) if f.endswith('.iml') or f == '.idea' or f == 'pom.xml' or f == 'build.gradle']

    return len(project_files)


def list_intellij_projects(path):
    intellij_dirs = [d for d in list_dirs(path) if is_intellij_project(path, d)]
    return intellij_dirs


def main(wf):
    projects_path = '/Users/geipette/projects'
    for intellij_dir in list_intellij_projects(projects_path):
        wf.add_item(title=intellij_dir,
                    arg=projects_path + '/' + intellij_dir,
                    subtitle=projects_path + '/' + intellij_dir,
                    valid=True)

    wf.send_feedback()


if __name__ == '__main__':
    sys.exit(main(Workflow()))
