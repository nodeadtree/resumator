import jinja2
import json
import os
import pathlib
import argparse

from jinja2 import Template
# V0 stuff.
# [x] Get the template directory
# [x] Make the resume json
# [x] Start filling out the tex template
# [x] Work on the CLI interface
# [x] Refactor into relevant pieces

# V0.1 stuff
# [x] Make template prettier and have it fit a single page
# [ ] Add checks for sections and formatting
# [ ] Add documentation for the json requirements
# [ ] Handle conditional rendering of sections in basic template
# [ ] Add CLI options for filtering sections

# V0.2 stuff
# [ ] Refactor __main__.py into separate sections and add some testing
# [ ] Refactor template into subfiles


def filter_text(text):
    substitutions = {
        '&': '\&',
        '_': '\\TextUnderscore '
    }

    def substitutor(char):
        if char in substitutions:
            return substitutions[char]
        return char
    return "".join(map(substitutor, text))


def filter_value(value):
    # Oy vey
    if isinstance(value, dict):
        return filter_json(value)
    elif isinstance(value, list):
        return list(map(filter_value, value))
    elif isinstance(value, str):
        return filter_text(value)
    else:
        return value


def filter_json(json):
    filtered_json = dict()
    for i in json:
        filtered_json[i] = filter_value(json[i])
    return filtered_json


def parse_json(path):
    with open(path, 'r') as raw_json:
        return json.load(raw_json)


def prepare_skill(skill):
    name = skill['name']
    years = skill['years']
    skill_string = f'{name} - {years} year'
    if skill['years'] > 1:
        skill_string += 's'
    if "location" in skill:
        location = skill["location"]
        skill_string += '\n\n{\\textit{'+location+'}}'
    return skill_string


def prepare_skill_section(raw_skills):
    return {section: [prepare_skill(i) for i in raw_skills[section]] for section in raw_skills}


def fill_template(experience_json, template):
    filled_template = template.render(
        personal_info=experience_json['personal_info'],
        skills=experience_json['skills'],
        experience=experience_json['experience'],
        education_section=experience_json['education'],
        projects=experience_json['projects']
    )
    return filled_template


def cli_wrapper():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-j", "--json", help="experience and skills json", required=True)
    parser.add_argument("-t", "--template",
                        help="template directory", required=True)
    parser.add_argument("-o", "--output", help="output file",
                        nargs="?", default='')
    args = parser.parse_args()
    template_path = pathlib.Path(args.template)
    template_dir = template_path.parent
    template = template_path.name
    latex_jinja_env = jinja2.Environment(
        block_start_string='\BLOCK{',
        block_end_string='}',
        variable_start_string='\VAR{',
        variable_end_string='}',
        comment_start_string='\#{',
        comment_end_string='}',
        line_statement_prefix='%%',
        line_comment_prefix='%#',
        lstrip_blocks=True,
        trim_blocks=True,
        autoescape=False,
        loader=jinja2.FileSystemLoader(template_dir)
    )
    parsed_json = filter_json(parse_json(args.json))
    jinja_template = latex_jinja_env.get_template(template)
    resume_tex = fill_template(parsed_json, jinja_template)
    if not args.output:
        print(resume_tex)
    else:
        print("not ready for this shit")


cli_wrapper()
