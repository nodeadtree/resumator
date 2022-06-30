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
# [ ] Add CLI options for filtering sections - probably going to have to do
# some somewhat serious changes to make this more ergonomic. I'm guessing that
# I did something weird to quickly generate a resume for when I applied to Juni

# V0.2 stuff
# [ ] Refactor __main__.py into separate sections and add some testing
# [ ] Refactor template into subfiles


# PROBABLY DEPRECATED - My guess is that these are temporarily dead code as a
# consequence of trying to generate a resume quickly for Juni
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


# PROBABLY DEPRECATED - My guess is that these are temporarily dead code as a
# consequence of trying to generate a resume quickly for Juni
def prepare_skill_section(raw_skills):
    return {section: [prepare_skill(i) for i in raw_skills[section]] for section in raw_skills}


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


def select_value(value):
    # Oy vey
    if isinstance(value, dict):
        return format_json(value)
    elif isinstance(value, list):
        return list(map(select_value, value))
    elif isinstance(value, str):
        return filter_text(value)
    else:
        return value


def format_json(json):
    filtered_json = dict()
    for i in json:
        filtered_json[i] = select_value(json[i])
    print(filtered_json)
    return filtered_json


def parse_json(path):
    with open(path, 'r') as raw_json:
        return json.load(raw_json)


def fill_template(experience_json, template):
    filled_template = template.render(
        personal_info=experience_json['personal_info'],
        skills=experience_json['skills'],
        experience=experience_json['experience'],
        # slightly temporary i believe
        education_section=experience_json['education'],
        # This lambda is temporary, until I remember the more general structure for the input.
        # reaaaaally should have made sure that I had documentation down for
        # the JSON formatting before I went awol on this project.
        projects=filter(lambda x: x['name'] not in ['MarkyMarkov'], experience_json['projects']
                        ))
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
    parsed_json = format_json(parse_json(args.json))
    jinja_template = latex_jinja_env.get_template(template)
    resume_tex = fill_template(parsed_json, jinja_template)
    if not args.output:
        print('no')
        # print(resume_tex)
    else:
        print("not ready for this shit")


if __name__ == "__main__":
    cli_wrapper()
