#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# TODO: create input form to get username password, confirm password, and email
# TODO: ensure valid email
# TODO: check if username is vaild, cannot contain space
# TODO: ensure passwords match

# TODO: post errors next to input boxes
# TODO: fill in boxes with user info



import webapp2
import re


#using re to check valid email, username, password, characters
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
   return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)



# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>User Sign-up</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <h1>User Sign-up</h1>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

# signup form html
form ="""
<form method= "post">
    <tabel>
        <tr>
            <td><label>
                Username:
                <input type="text" name="username" value="%(username)s">
                </td>
                <td><span class="error">%(us_error)s</span>
            </label></td>
        </tr>
        <br>
        <tr>
            <td><label>
                Password:
                <input type="password" name="password" value="">
                </td>
                <td><span class="error">%(pw_error)s</span>
            </label></td>
        </tr>
        <br>
        <tr>
            <td><label>
                Confirm Password:
                <input type="password" name="conf_password" value="">
                </td>
                <td><span class="error">%(conf_error)s</span>
            </label></td>
        </tr>
        <br>
        <tr>
            <td><label>
                Email:
                <input type="email" name="email" value=%(email)s>
                </td>
                <td><span class="error">%(em_error)s</span>
            </label></td>
        </tr>
        <br>
    </table>
    <input type="submit">
</form>
"""
content = page_header + form + page_footer



#index page gets with form
class Index(webapp2.RequestHandler):
    def write_form(self, us_error="", pw_error="", conf_error="", em_error="", username="", email=""):
      self.response.write(content % {"us_error": us_error,
                                     "pw_error" : pw_error,
                                     "conf_error": conf_error,
                                     "em_error" : em_error,
                                     "username" : username,
                                     "email" : email})


    def get(self):
        self.write_form()

    def post(self):

      have_error = False

      #set blank strings for error messages
      us_error=""
      pw_error=""
      conf_error=""
      em_error=""

      #get info from form
      username = self.request.get('username')
      password = self.request.get('password')
      conf_password = self.request.get('conf_password')
      email = self.request.get('email')

      #validation of entries and addition of error statements if entries are not vaild
      if not valid_username(username):
        us_error = "That is not a vaild username."
        have_error = True


      if not valid_password(password):
        pw_error = "That is not a vaild password."
        have_error = True


      elif password != conf_password:
        conf_error = "Your passwords do not match."
        have_error = True


      if not valid_email(email):
        error_email = "That's not a vaild email."
        have_error = True


      #if there are error rewrite form with these variables passed back in
      if have_error:
        self.write_form(us_error, pw_error, conf_error, em_error, username, email)


      #if everything is good, redirect to new page
      else:
        self.redirect("/thanks?username=" + username)


#handler class for new page, displays username
class Thanks(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")
        self.response.write("Thanks for signing up " + username +"!")



app = webapp2.WSGIApplication([
    ('/', Index),
    ('/thanks', Thanks)
], debug=True)
