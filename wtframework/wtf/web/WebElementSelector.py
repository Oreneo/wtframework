##########################################################################
#This file is part of WTFramework. 
#
#    WTFramework is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    WTFramework is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with WTFramework.  If not, see <http://www.gnu.org/licenses/>.
##########################################################################
'''
Created on Feb 11, 2013

@author: "David Lai"
'''
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotSelectableException



class WebElementSelector():
    
    @staticmethod
    def find_element_by_selectors(webdriver, *selectors):
        """
        Utility method makes it easier to find an element using multiple selectors. This is 
        useful for problematic elements what might works with one browser, but fail in another.
        
        Usage:
            my_element = WebElementSelector.find_element_by_selectors(webdriver,
                                                                    (By.ID, "MyElementID"),
                                                                    (By.CSS, "MyClassSelector") )

        @param webdriver: Selenium WebDriver.
        @param selectors: Selectors as a variable arg list of (By, value) pairs.
        """
        #perform initial check to verify selectors are valid by statements.
        for selector in selectors:
            (by_method, value) = selector
            if not WebElementSelector.__is_valid_by_type(by_method):
                raise BadSelectorError("Selectors should be of type selenium.webdriver.common.by.By")
            if type(value) != str:
                raise BadSelectorError("Selectors should be of type selenium.webdriver.common.by.By")
        
        selectors_used = []
        for selector in selectors:
            (by_method, value) = selector
            selectors_used.append("{by}:{value}".format(by=by_method, value=value))
            try:
                return webdriver.find_element(by=by_method, value=value)
            except:
                pass
        
        raise ElementNotSelectableException("Unable to find elements using:" + ",".join(selectors_used))
    
    @staticmethod
    def __is_valid_by_type(by_type):
        for attr, value in By.__dict__.iteritems():
            if "__" not in attr:
                if by_type == value:
                    return True
        
        return False

class BadSelectorError(Exception):
    "Raised when a bad selector is passed into a WebElementSelector() method."
    pass