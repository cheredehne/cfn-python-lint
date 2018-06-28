"""
  Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.

  Permission is hereby granted, free of charge, to any person obtaining a copy of this
  software and associated documentation files (the "Software"), to deal in the Software
  without restriction, including without limitation the rights to use, copy, modify,
  merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
  permit persons to whom the Software is furnished to do so.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
  PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
  HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
  OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
  SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import re
from cfnlint import CloudFormationLintRule
from cfnlint import RuleMatch

class SecurityGroupDescription(CloudFormationLintRule):
    """Check SecurityGroup Description Configuration"""
    id = 'E2509'
    shortdesc = 'Validate SecurityGroup description'
    description = 'Check if SecurityGroup descriptions are correctly configured'
    tags = ['base', 'resources', 'securitygroup']

    description_regex = r'^([a-z,A-Z,0-9,. _\-:/()#,@[\]+=&;\{\}!$*])*$'

    def check_value(self, value, path):
        """Check SecurityGroup descriptions"""
        matches = list()
        full_path = ('/'.join(str(x) for x in path))

        # Check max length
        if len(value) > 255:
            message = 'GroupDescription length ({0}) exceeds the limit (255) at {1}'
            matches.append(RuleMatch(path, message.format(len(value), full_path)))
        else:
            # Check valid characters
            regex = re.compile(self.description_regex)
            if not regex.match(value):
                message = 'GroupDescription contains invalid characters (valid characters are: '\
                          '"a-zA-Z0-9. _-:/()#,@[]+=&;\\{{}}!$*"") at {0}'
                matches.append(RuleMatch(path, message.format(full_path)))

        return matches

    def match(self, cfn):
        """Check SecurityGroup descriptions"""

        matches = list()

        resources = cfn.get_resources(['AWS::EC2::SecurityGroup'])

        for resource_name, resource in resources.items():
            path = ['Resources', resource_name, 'Properties']

            properties = resource.get('Properties')
            if properties:
                matches.extend(
                    cfn.check_value(
                        properties, 'GroupDescription', path,
                        check_value=self.check_value, check_ref=None,
                        check_find_in_map=None, check_split=None, check_join=None
                    )
                )

        return matches
