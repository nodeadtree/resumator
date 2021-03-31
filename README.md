# Resumator
Extremely WIP resume generation script

Rough roadmap
## V0 stuff.
- [x] Get the template directory
- [x] Make the resume json (it's not available here, sorry!)
- [x] Start filling out the tex template
- [x] Work on the CLI interface
- [x] Refactor into relevant pieces

## V0.1 stuff
- [x] Make template prettier and have it fit a single page
- [ ] Add checks for sections and formatting
- [ ] Add documentation for the json requirements
- [ ] Handle conditional rendering of sections in basic template
- [ ] Add CLI options for filtering sections

## V0.2 stuff
- [ ] Refactor __main__.py into separate sections and add some testing
- [ ] Refactor template into subfiles
- [ ] Fill out readme


## Experience JSON

The experience JSON has a few expected sections, and a full example is included in the 
examples directory


The first expected entry is the personal info entry , basic stuff like contact
information and the like belongs here. This entry should look like the
following
```
  "personal_info": {
    "first_name": "Juniper",
    "last_name": "Overbeck",
    "email": "nodeadtree@gmail.com",
    "website": "www.nodeadtree.com",
    "github": "www.github.com/nodeadtree"
  },
```
Next is the education section, it's going to be an array/list of credentials
and where they came from, each education entry should have at least the
following fields:
```
    {
      "title": "MS Pure Mathematics",
      "school": "SFSU",
      "time": "Spring 2020"
    },
  ]
```
- title should be the name of the credential
- school should be where you got the credential
- time should be when the credential was given


This is roughly what skills section looks like for now, but this is the area
that is most likely to change tl;dr

skills is an object,
keys in that object correspond to a type of skill, the values associated with
those keys are arrays containing skill objects which have:
- name: should be the name of the skill
- years: amount of experience with that skill
- description: plain text description, included as a subtitle underneath the
  skill itself
```
  "skills": {
    "Languages": [
      {
        "name": "Python",
        "years": 8,
        "description": "used for all sorts of stuff"
      },
    ]
  }
```
The experience section should be an array of objects, each of the objects has
roughly the following keys
- employer: name of the employer
- title: job title
- subtitle: it's a subtitle
- start: start of job
- end: end of job
- bullets: complete sentences describing some of the responsibilities
```
  "experience": [
    {
      "employer": "Divvy Homes",
      "title": "Software Engineer",
      "subtitle": "Full Stack Web Development",
      "start": "08/26/2019",
      "end": "05/8/2020",
      "bullets": [
        "Implemented internal A/B testing framework",
        "Documented and formalized existing engineering practices",
        "Refactored existing React components to use contexts and hooks",
        "Simplified our approach to pairing agents with customers",
        "Led a weekly reading group on mathematics"
      ]
    },
  ],
```
The projects section resembles the experience section
- name: name of the project
- subtitle: subtitle to put under the name
- bullets: complete sentences used to describe the project
```
  "projects": [
    {
      "name": "tetucyc",
      "subtitle": "Configurable tool for automating classifier tests",
      "bullets": [
        "Used to automate the tuning and training of classifiers",
        "Works with any dimension of correctly formatted data",
        "Can work with arbitrary classifiers",
        "Can accept arbitrary parameter search areas",
        "Can restrict testing to a user selected subset of classes"
      ]
    },
  ]
```

## Notes on the experience json
The skills section should be completely undone and merged with the experience
section, and the script should handle the calculation of how much experience
the user has with a given skill
