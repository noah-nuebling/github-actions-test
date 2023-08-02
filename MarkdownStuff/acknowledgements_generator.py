
#!/usr/bin/python

#
# Imports
#
import sys
import argparse
import requests
import json
import pycountry
import datetime

#
# Constants
#
# (We expect this script to be run from the root directory of the repo)

template_path = "MarkdownStuff/acknowledgements_template.md"
destination_path = "Acknowledgements.md"
gumroad_product_ids = ["FP8NisFw09uY8HWTvVMzvg==", "OBIdo8o1YTJm3lNvgpQJMQ=="] # 2nd product is mmfinappusd
gumroad_api_base = "https://api.gumroad.com"
gumroad_sales_api = "/v2/sales"

#
# Main
#
def main():
    
    # Parse args
    #   Get Gumroad API key
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--api_key")
    args = parser.parse_args()
    gumroad_api_key = args.api_key

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
    
    print('Filtering sales...')
    # print(json.dumps(sales, indent=2))
    
    # Filter people who don't want to be displayed
    
    print('')
    sales = list(filter(wants_display, sales))
    print('')
    
    # Filter generous and very generous
    
    generous_sales = list(filter(is_generous, sales))
    very_generous_sales = list(filter(is_very_generous, sales))
    
    # Log
    print('Compiling generous contributor strings...')
    
    # Generate generous markdown
    
    generous_string = ''
    first_iteration = True
    for sale in generous_sales:
        
        if not first_iteration:
            generous_string += ' | '
        first_iteration = False
        
        generous_string += display_name(sale)

    # Generate very generous markdown
    
    very_generous_string = ''
    last_month = None
    first_iteration = True
    
    for sale in very_generous_sales:
        date_string = sale['created_at']
        date = datetime.datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ') # T means nothing, Z means UTC+0
        if date == None:
            print('Couldnt extract date from string {}'.format(date_string))
            exit(1)
        
        if date.month != last_month:
            
            last_month = date.month
            
            if not first_iteration:
                very_generous_string += '\n\n'
            first_iteration = False
            
            very_generous_string += '__{}__\n'.format(date.strftime('%B %Y')) # %B -> Month %Y -> Year
        
        very_generous_string += '\n- ' + display_name(sale)
        
    # Log
    
    print('\nGenerous string:\n\n{}\n'.format(generous_string))
    print('Very Generous string:\n\n{}\n'.format(very_generous_string))
    
    # print(len(list(map(lambda sale: sale['email'], generous_sales))))
    # print(len(list(map(lambda sale: sale['email'], very_generous_sales))))
    
    # Log
    print('Inserting generous contributor strings into template at {}...'.format(template_path))
    
    # Load template
    template = ""
    with open(template_path) as f:
        template = f.read()
    
    # Insert into template
    template = template.format(generous = generous_string, very_generous = very_generous_string, sales_count = all_sales_count)
    
    # Write template
    with open(destination_path, "w") as f:
        f.write(template)
    
    # Log
    print('Wrote result to {}'.format(destination_path))
    
    
# 
# Helper 
#
 
def display_name(sale):
    
    name = ''
    
    if 'full_name' in sale:
        name = sale['full_name']
    
    if name == '':
        email = ''
        if 'email' in sale:
            email = sale['email']
        elif 'purchase_email' in sale:
            email = sale['purchase_email']
        else:
            sys.exit(1)
        name = email.partition('@')[0]

    name = name.title().replace('.', ' ')

    flag = emoji_flag(sale)
    if flag != '':
        name = flag + ' ' + name
    
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
    if sale['variants_and_quantity'] == '(2. Option)':
        return True
    if sale['formatted_display_price'] == '€5':
        return True
    if sale['formatted_display_price'] == '$5':
        return True
    
    return False
 
def is_very_generous(sale):
    if sale['variants_and_quantity'] == '(3. Option)':
        return True
    if sale['formatted_display_price'] == '€10':
        return True
    if sale['formatted_display_price'] == '$10':
        return True
    
    return False
        
def wants_display(sale):
    if sale['has_custom_fields']: # !! Update this if you change UI string on Gumroad !!
        if sale['custom_fields'].get("Don't publicly display me as a 'Generous Contributor' under 'Acknowledgements'", False) == True:
            print("{} payed {} but does not want to be displayed".format(display_name(sale), sale['formatted_display_price']))
            return False
    return True

#
# Call main
#
if __name__ == "__main__":
    main()
