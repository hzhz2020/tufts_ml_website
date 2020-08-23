'''
'''

import pandas as pd
import datetime

today_timestamp = datetime.datetime.today().strftime('%Y-%m-%d')

## TODO to add more event sections just update this list
semname_and_csvfile_pairs = [
    ('Fall 2020', 'courses_2020_fall.csv'),
    ('Spring 2020', 'courses_2020_spring.csv'),
    ('Fall 2019', 'courses_2019_fall.csv'),
    ('Spring 2019', 'courses_2019_spring.csv'),
    ('Fall 2018', 'courses_2018_fall.csv'),
    ('Spring 2018', 'courses_2018_spring.csv'),
    ]

main_item_template_str = \
"""
    <div class="row row-striped">
        <div class="d-none d-sm-block col-sm-2 text-right">
            <img src="{{COURSE_IMG}}" class="img-fluid mw-100" alt="Responsive image">
        </div>
        <div class="col-12 col-sm-10">
            <h3>
            <a href="{{COURSE_URL}}">
                <strong>
                    {{COURSE_NUM}}: {{COURSE_TITLE}}
                </strong>
            </a>
            </h3>
            <p>
            Instructor: {{INSTRUCTOR}}
            </p>
        </div>
    </div>
\n"""



out_md_str = "Title: Courses \nDate: %s\nsave_as: courses.html" % (
    today_timestamp)

out_md_str += (
"""\n
<!-- THIS PAGE SRC IS AUTO GENERATED. At terminal: $ make courses_page -->


Below you can find a listing of courses in the Tufts CS department related to Machine Learning.

\n""")


for sec_title, csv_fpath in semname_and_csvfile_pairs:

    csv_df = pd.read_csv(csv_fpath)
    csv_df = csv_df.fillna('') # Fill missing values with blanks
    assert csv_df.shape[0] > 0

    anchor = sec_title.lower().replace(' ', '-')
    out_md_str += "\n<a name='%s'></a>" % (anchor)
    out_md_str += "\n<h2>Courses: %s</h2>" % (sec_title)

    ## Main team names, images, + links
    out_md_str += '\n\n\n<div class="container">'
    for item_id, (row_id, row_df) in enumerate(csv_df.iterrows()):
        row_dict = row_df.to_dict()
        item_str = main_item_template_str + ""
        for key, val in row_dict.items():
            if key.count('URL'):
                default_val = "#"
            else:
                default_val = ""
            cur_val = str(val)
            if len(cur_val) == '' or cur_val == 'nan':
                cur_val = default_val
            item_str = item_str.replace("{{%s}}" % str(key), cur_val)
        out_md_str += item_str
    out_md_str += "</div>\n"

with open("../pages/courses.md", 'w') as f:
    f.write(out_md_str)
