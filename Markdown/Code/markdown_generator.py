#
# Imports
#
import sys
import argparse
import requests
# import json
import pycountry
import datetime
import babel.dates
import pathlib
import urllib.parse
import string

#
# Constants
#
# (We expect this script to be run from the root directory of the repo)

documents = {
    
    "readme": [
        {
            "language_name": "🇬🇧 English", # Language name will be displayed in the language picker
            "language_tag": "en-US",
            "template_path": "Markdown/Templates/readme_template_en-US.md",
            "destination_path": "Readme.md"
        },
        {
            "language_name": "🇩🇪 Deutsch",
            "language_tag": "de-DE",
            "template_path": "Markdown/Templates/readme_template_de-DE.md",
            "destination_path": "Markdown/LocalizedDocuments/Readme - 🇩🇪 Deutsch.md"
        },
    ],
    "acknowledgements": [
        {
            "language_name": "🇬🇧 English", # Language name will be displayed in the language picker
            "language_tag": "en-US", # Used to autogenerate some localized text (at time of writing only month names in the 'very generous' string). Find language tags here: https://www.techonthenet.com/js/language_tags.php
            "template_path": "Markdown/Templates/acknowledgements_template_en-US.md",
            "destination_path": "Acknowledgements.md"
        },
        {
            "language_name": "🇩🇪 Deutsch",
            "language_tag": "de-DE",
            "template_path": "Markdown/Templates/acknowledgements_template_de-DE.md",
            "destination_path": "Markdown/LocalizedDocuments/Acknowledgements - 🇩🇪 Deutsch.md"
        },
    ]
}
    

# !! Amend these if you change the UI strings on Gumroad !!
gumroad_user_name_labels = ["Your Name – Will be displayed in the Acknowledgements if you purchase the 2. or 3. Option"]
gumroad_custom_message_labels = ["Your message (Will be displayed next to your name in the Acknowledgements if you purchase the 3. Option)", "Your message – Will be displayed next to your name in the Acknowledgements if you purchase the 3. Option"]
gumroad_dont_display_labels = ["Don't publicly display me as a 'Generous Contributor' under 'Acknowledgements'"]

gumroad_product_ids = ["FP8NisFw09uY8HWTvVMzvg==", "OBIdo8o1YTJm3lNvgpQJMQ=="] # 1st is is the € based product (Which we used in the earlier MMF 3 Betas, but which isn't used anymore), 2nd id is $ based product (mmfinappusd)
gumroad_api_base = "https://api.gumroad.com"
gumroad_sales_api = "/v2/sales"
gumroad_date_format = '%Y-%m-%dT%H:%M:%SZ' # T means nothing, Z means UTC+0 | The date strings that the gumroad sales api returns have this format
name_blacklist = ['mail', 'paypal', 'banking', 'it-beratung', 'macmousefix'] # When gumroad doesn't provide a name we use part of the email as the display name. We use the part of the email before @, unless it contains one of these substrings, in which case we use the part of the email after @ but with the `.com`, `.de` etc. removed
nbsp = '&nbsp;'  # Non-breaking space. &nbsp; doesn't seem to work on GitHub. Tried '\xa0', too. See https://github.com/github/cmark-gfm/issues/346


#
# Main
#
def main():
    
    # Parse args
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--document")
    parser.add_argument("--api_key")
    parser.add_argument("--no_api", action='store_true')
    args = parser.parse_args()
    gumroad_api_key = args.api_key
    document_tag = args.document
    no_api = args.no_api
    
    # Validate
    document_tag_was_provided = isinstance(document_tag, str) and document_tag != ''
    if not document_tag_was_provided:
        print("No document tag provided. Provide one using the '--document' command line argument.")
        sys.exit(1)
    document_tag_is_valid = document_tag in documents.keys()
    if not document_tag_is_valid:
        print(f"Unknown document tag '{document_tag}'. Valid document tags: {list(documents.keys())}")
        sys.exit(1)
    
    # Iterate language dicts

    language_dicts = documents[document_tag]
    
    for language_dict in language_dicts:
        
        # Extract info from language_dict
        template_path = language_dict['template_path']
        destination_path = language_dict['destination_path']
        
        # Load template
        template = ""
        with open(template_path) as f:
            template = f.read()
        
        # Log
        print('Inserting generated strings into template at {}...'.format(template_path))
        
        # Insert into template
        if document_tag == "readme":
            template = insert_root_paths(template, language_dict)
            template = insert_language_picker(template, language_dict, language_dicts)
        elif document_tag == "acknowledgements":
            template = insert_root_paths(template, language_dict) # This is not currently necessary here since we don't use the {root_path} placeholder in the acknowledgements templates
            template = insert_language_picker(template, language_dict, language_dicts)
            template = insert_acknowledgements(template, language_dict, gumroad_api_key, no_api)
        else:
            assert False # Should never happen because we check document_tag for validity above.
        
        # Validate that template is completely filled out
        template_parse_result = list(string.Formatter().parse(template))
        template_fields = [tup[1] for tup in template_parse_result if tup[1] is not None]
        is_fully_formatted = len(template_fields) == 0
        if not is_fully_formatted:
            print(f"Something went wrong. Template at '{template_path}' still has format field(s) after inserting: {template_fields}")
            sys.exit(1)
        
        # Add comment to the top of the document which says that it is autogenerated
        template = "<!-- THIS FILE IS AUTOMATICALLY GENERATED - EDITS WILL BE OVERRIDDEN -->\n" + template
        
        # Write template
        with open(destination_path, mode="w") as f:
            f.write(template)
        
        # Log
        print('Wrote result to {}'.format(destination_path))
    
    
# 
# Template inserters 
#

sales_data_cache = None

def insert_acknowledgements(template, language_dict, gumroad_api_key, no_api):
    
    if no_api:
        template = template.replace('{very_generous}', 'NO_API').replace('{generous}', 'NO_API').replace('{sales_count}', 'NO_API')
        return template
    
    global sales_data_cache
    
    all_sales_count = None
    generous_sales = None
    very_generous_sales = None
    
    if sales_data_cache != None:
        
        #
        # Load from cache
        #
        
        all_sales_count = sales_data_cache['all_sales_count']
        generous_sales = sales_data_cache['generous_sales']
        very_generous_sales = sales_data_cache['very_generous_sales']
        
    else: 
        
        #
        # Load from scratch and store in cache
        #
    
        # Load all sales of the gumroad product
        
        sales = []
        
        for pid in gumroad_product_ids:
            
            page = 1
            api = gumroad_sales_api

            while True:
                
                print('Fetching sales for product {} page {}...'.format(pid, page))
                
                response = requests.get(gumroad_api_base + api, 
                            headers={'Content-Type': 'application/x-www-form-urlencoded'},
                            params={'access_token': gumroad_api_key,
                                    'product_id': pid})
                
                if response.status_code != 200:
                    print('HTTP request failed with code: {}'.format(response.status_code))
                    if response.status_code == 401:
                        print('(The request failed because it is unauthorized (status 401). This might be because you are not providing a correct Access Token using the `--api_key` command line argument. You can retrieve an Access Token in the GitHub Secrets or in the Gumroad Settings under Advanced.')
                    sys.exit(1)

                response_dict = response.json()
                if response_dict['success'] != True:
                    print('Gumroad API returned failure')
                    sys.exit(1)
                
                sales += response_dict['sales']
                
                if 'next_page_url' in response_dict:
                    api = response_dict['next_page_url']
                else:
                    break
                
                page += 1
        
        # Record all sales count
        
        all_sales_count = len(sales)
        
        # Log
        
        print('Sorting and filtering sales...')
        # print(json.dumps(sales, indent=2))
        
        # Filter people who don't want to be displayed
        
        print('')
        sales = list(filter(wants_display, sales))
        print('')
        
        # Sort sales by date
        sales.sort(key=(lambda sale: datetime.datetime.strptime(sale['created_at'], gumroad_date_format)), reverse=True)
        
        # Filter generous and very generous
        generous_sales = list(filter(is_generous, sales))
        very_generous_sales = list(filter(is_very_generous, sales))
    
        # Create cache and store in cache
        sales_data_cache = dict()
        sales_data_cache['all_sales_count'] = all_sales_count
        sales_data_cache['generous_sales'] = generous_sales
        sales_data_cache['very_generous_sales'] = very_generous_sales
    
    # Log
    print('Compiling generous contributor strings...')
    
    # Generate generous markdown
    
    generous_string = ''
    first_iteration = True
    for sale in generous_sales:
        
        if not first_iteration:
            generous_string += nbsp + '| '
        first_iteration = False
        
        generous_string += display_name(sale)

    # Generate very generous markdown
        
    very_generous_string = ''
    
    language_tag = language_dict['language_tag']
    
    last_month = None
    first_iteration = True
    
    for sale in very_generous_sales:
        date_string = sale['created_at']
        date = datetime.datetime.strptime(date_string, gumroad_date_format)
        if date == None:
            print('Couldnt extract date from string {}'.format(date_string))
            exit(1)
        
        if date.month != last_month:
            
            last_month = date.month
            
            if not first_iteration:
                very_generous_string += '\n\n'
            first_iteration = False
            
            very_generous_string += '__{}__\n'.format(babel.dates.format_datetime(datetime=date, format='LLLL yyyy', locale=language_tag.replace('-', '_'))) # See https://babel.pocoo.org/en/latest/dates.html and https://babel.pocoo.org/en/latest/api/dates.html#babel.dates.format_datetime. For some reason, babel wants _ instead of - in the language tags, not sure why.
        
        name = display_name(sale)
        message = user_message(sale)
        
        if len(message) > 0:
            very_generous_string += '\n- ' + name + f' - *"{message}"*'
        else:
            very_generous_string += '\n- ' + name
    
    # Log
    print('\nGenerous string:\n\n{}\n'.format(generous_string))
    print('Very Generous string:\n\n{}\n'.format(very_generous_string))
    
    print('Inserting into template:\n\n{}\n'.format(template))
    
    # Insert into template
    # str.format forces us to replace all the template placeholders at once, which we don't want, so we use str.replace
    
    # template = template.format(very_generous=very_generous_string, generous=generous_string, sales_count=all_sales_count)
    template = template.replace('{very_generous}', very_generous_string).replace('{generous}', generous_string).replace('{sales_count}', str(all_sales_count))
    
    # Return
    return template
    
def insert_language_picker(template, language_dict, language_dicts):
        
    # Extract info from language_dict
        
    language_name = language_dict['language_name']
    
    # Generate language list ui string
    
    ui_language_list = ''
    for i, language_dict2 in enumerate(language_dicts):
        
        is_last = i == len(language_dicts) - 1
        
        language_name2 = language_dict2['language_name']
        
        # Create relative path from the location of the `language_dict` document to the `language_dict2` document. This relative path works as a link. See https://github.blog/2013-01-31-relative-links-in-markup-files/
        path = language_dict['destination_path']
        path2 = language_dict2['destination_path']
        root_path = path_to_root(path)
        relative_path = root_path + path2
        link = urllib.parse.quote(relative_path) # This percent encodes spaces and others chars which is necessary
        
        ui_language_list += '  '
        
        if language_name == language_name2:
            ui_language_list += f'**{language_name2}**'
        else:
            ui_language_list += f'[{language_name2}]({link})'
        
        ui_language_list += '\\'
        if not is_last: 
            ui_language_list += '\n'
        
    # Log    
    print(f'\nLanguage picker language list generated for language "{language_name}":\n{ui_language_list}\n')
    # print('Inserting into template:\n\n{}\n'.format(template))
    
    # Insert generated strings into template
    # template = template.format(current_language=language_name, language_list=ui_language_list)
    template = template.replace('{current_language}', language_name).replace('{language_list}', ui_language_list)
    
    # Return
    return template

def insert_root_paths(template, language_dict):
        
    # Extract info from language_dict
        
    path = language_dict['destination_path']
    template = template.replace('{repo_root}', path_to_root(path))
    
    return template

# 
# Particle generators
#
 
def path_to_root(path):
    parent_count = len(pathlib.Path(path).parents)
    root_path = ('../' * (parent_count-1))
    return root_path
 
def display_name(sale):
    
    name = ''
    
    # Get user-provided name field
    #   We haven't tested this so far due to laziness
    if sale['has_custom_fields']:
        for label in gumroad_user_name_labels:
            name = sale['custom_fields'].get(label, '')
            if name != '':
                break
    
    # Get full_name field
    if name == '':
        if 'full_name' in sale:
            name = sale['full_name']
    
    # Fallback to email-based heuristic
    if name == '':
        email = ''
        if 'email' in sale:
            email = sale['email']
        elif 'purchase_email' in sale:
            email = sale['purchase_email']
        else:
            sys.exit(1)
        
        n1, _, n2 = email.partition('@')
        
        use_n1 = True
        for non_name in name_blacklist:
            if non_name in n1:
                use_n1 = False
                break
        
        if use_n1:
            name = n1
        else:
            name = n2.partition('.')[0] # In a case like gm.ail.com, we want gm.ail, but this will just return gm. But should be good enough.

    # Replace weird separators with spaces
    for char in '._-–—+':
        name = name.replace(char, ' ')

    # Capitalize
    name = name.title()
    
    # Prepend flag
    flag = emoji_flag(sale)
    if flag != '':
        name = flag + ' ' + name
    
    # Replace all spaces with non-breaking spaces
    name = name.replace(' ', nbsp)
    
    return name
 
def emoji_flag(sale):
    
    country_code = sale.get('country_iso2', '')
    if country_code == '':
        country_code = pycountry.countries.get(name=sale.get('country', '')).alpha_2
    
    if country_code == '':
        return ''
    
    result = ''
    for c in country_code.upper():
        result += chr(ord(c) + 127397)
    return result
 
def is_generous(sale):
    
    sale_pid = sale['product_id']
    euro_pid = gumroad_product_ids[0]
    dollar_pid = gumroad_product_ids[1]
    
    if sale_pid == euro_pid:
        if sale['variants_and_quantity'] == '(2. Option)': 
            return True
        if sale['formatted_display_price'] == '€5': # Commenting this out doesn't change the results. Not sure why we wrote this - maybe the "variants_and_quantity" value used to be different from (2. Option) for a period?
            return True
    elif sale_pid == dollar_pid:
        if sale['variants_and_quantity'] == '(2. Option)':
            return True
    else:
        assert False
    
    return False
 
def is_very_generous(sale):
    
    sale_pid = sale['product_id']
    euro_pid = gumroad_product_ids[0]
    dollar_pid = gumroad_product_ids[1]
    
    if sale_pid == euro_pid:
        if sale['variants_and_quantity'] == '(3. Option)':
            return True
        if sale['formatted_display_price'] == '€10': # Commenting this out doesn't change the results
            return True
    elif sale_pid == dollar_pid:
        if sale['variants_and_quantity'] == '(3. Option)':
            return True
    else:
        assert False
        
    return False
        
def wants_display(sale):
    if sale['has_custom_fields']:
        for label in gumroad_dont_display_labels:
            if sale['custom_fields'].get(label, False) == True:
                print("{} payed {} and does not want to be displayed".format(display_name(sale), sale['formatted_display_price']))
                return False
    return True

def user_message(sale):
    
    message = ''
    if sale['has_custom_fields']:
        
        for label in gumroad_custom_message_labels:
            message = sale['custom_fields'].get(label, '')
            if len(message) > 0:
                break

    if len(message) > 0:
        print("{} payed {} and left message: {}".format(display_name(sale), sale['formatted_display_price'], message))
    
    return message

#
# Call main
#
if __name__ == "__main__":
    main()
