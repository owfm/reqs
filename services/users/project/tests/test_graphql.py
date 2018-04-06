from project.tests.base import BaseTestCase
# import json

import pprint

pp = pprint.PrettyPrinter(indent=4)


class TestGraphQL(BaseTestCase):
    """ test graph ql implementation """

    def test_graph_ql(self):
        """ test graphql can be used """

        with self.client:

            url = '/graphql?query={AllUsers {email}}'

            response = self.client.post(
                url
            )

            pp.pprint(response)
