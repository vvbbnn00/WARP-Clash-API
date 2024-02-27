"""

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <https://www.gnu.org/licenses>.

"""
import uuid

from faker import Faker


class NodeNameGenerator:
    """
    This class is used for generate unique node names
    """

    def __init__(self, random_name=True):
        self.random_name = random_name
        self.fake = Faker()
        self.used_names = set()
        self.counter = 1  # Used when random_name is False

    def generate_unique_name(self, country_emoji, country):
        """
        Generate unique node name
        :param country_emoji:
        :param country:
        :return:
        """
        name_type = 'color'
        cnt = 0  # Used to avoid infinite loop
        while True:
            if name_type == 'color':
                name = f"{country_emoji} {country}-CF-{self.fake.color_name()}"
                cnt += 1
                if cnt > 100:
                    name_type = 'alternate'  # If color name is not available, use alternate name
                    cnt = 0  # Reset counter
            elif name_type == 'alternate':
                name = f"{country_emoji} {country}-CF-{self.fake.city()}"  # When color name is not available
                cnt += 1
                if cnt > 100:
                    name_type = 'random'  # If alternate name is not available, use random name
                    cnt = 0
            else:  # When name_type is invalid
                name = f"{country_emoji} {country}-CF-{uuid.uuid4()}"  # Use UUID to ensure uniqueness

            if name not in self.used_names:
                self.used_names.add(name)
                return name

    def next(self, country_emoji, country):
        """
        Generate next node name
        :param country_emoji: Country emoji
        :param country: Country name
        :return: Node name
        """
        if self.random_name:
            # Try to generate a unique name, first try color name, then try alternate name
            return self.generate_unique_name(country_emoji, country)
        else:
            name = f"{country_emoji} {country}-CF-WARP-{self.counter}"
            self.counter += 1
            return name
