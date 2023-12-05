import csv


# read in the zips.csv and create dictionary using zip code as the key
# with value of tuple of state and rate_area
# remove zip codes that have more than one tuple
def make_zip_state_rate_area():
    with open('zips.csv', mode='r') as file:
        zips_reader = csv.DictReader(file)
        zips_data = list(zips_reader)

    # Create a dictionary to group records by zip code
    grouped_zip_data = {}

    for row in zips_data:
        zip_code = row['zipcode']
        state = row['state']
        rate_area = row['rate_area']

        # Use zip code as the key to group records
        key = zip_code
        if key not in grouped_zip_data:
            # Initialize a list for this (state, rate_area) combination
            grouped_zip_data[key] = set()
        grouped_zip_data[zip_code].add((state, rate_area))
    # Create a dictionary to store the final result with only one state and rate_area tuple per zip code
    # if a zip code has more than one unique tuple, ignore it
    final_zip_data = {}

    # Iterate through grouped_zip_data and keep only entries with one tuple
    for zip_code, tuples in grouped_zip_data.items():
        if len(tuples) == 1:
            # Return the tuple, since there is only one in this record
            final_zip_data[zip_code] = tuples.pop()
    return final_zip_data


# read in the plans.csv and create dictionary using
# tuple of state and rate_area for plans with metal_level
# of Silver
def rate_area_silver_multiple_plans():
    with open('plans.csv', mode='r') as file:
        plans_reader = csv.DictReader(file)
        plans_data = list(plans_reader)

    # Create a dictionary to group records by state and rate area
    grouped_data = {}

    for row in plans_data:
        if row['metal_level'] == "Silver":
            state = row['state']
            rate_area = row['rate_area']
            rate = row['rate']

            # Use a tuple of (state, rate_area) as the key to group records
            key = (state, rate_area)
            if key not in grouped_data:
                # Initialize a list for this (state, rate_area) combination
                grouped_data[key] = {
                    'state': state,
                    'rate_area': rate_area,
                    'rates': []
                }
            # Add the rate to the list of rates for this combination
            grouped_data[key]['rates'].append(rate)
    # Iterate through the grouped data
    for key, value in grouped_data.items():
        # Access the 'rates' list and remove duplicates
        unique_rates = list(set(float(rate) for rate in value['rates']))
        # take unique 'rates' list and sort it in ascending order
        value['rates'] = sorted(unique_rates)
    # Filter the grouped data to include records with more than one rate
    # and calculate the second-lowest cost for each record
    filtered_grouped_data = {}
    for key, value in grouped_data.items():
        if len(value['rates']) > 1:
            # Calculate the second lowest cost
            second_lowest_cost = sorted(value['rates'])[1]
            value['second_lowest_cost'] = second_lowest_cost
            filtered_grouped_data[key] = value
    return filtered_grouped_data


def final_lookup_and_output(plan_costs, zip_state_rate_area):
    # read the slscp.csv file into a dictionary
    with open('slcsp.csv', mode='r') as file:
        slcsp_reader = csv.DictReader(file)
        slcsp_data = list(slcsp_reader)

    print('zipcode,rate')
    for row in slcsp_data:
        zipcode = row['zipcode']
        # first check that the zip code in the slscp file has an entry in the make_zip_state_rate_area file
        # if entry exists, retrieve the tuple (state, rate_area)
        if zipcode in zip_state_rate_area:
            plan_rate_tuple = zip_state_rate_area[zipcode]
            if plan_rate_tuple in plan_costs:
                output_plan_cost = plan_costs[plan_rate_tuple]
                formatted_string = f"{zipcode},{output_plan_cost['second_lowest_cost']}"
                print(formatted_string)
            else:
                # one Sliver plan or no Silver plans in this rate plan tuple, return a blank
                formatted_string = f"{zipcode},"
                print(formatted_string)
        else:
            # no unique state and rate_area tuple, return a blank
            formatted_string = f"{zipcode},"
            print(formatted_string)


def main():
    plan_costs = rate_area_silver_multiple_plans()
    zip_state_rate_area = make_zip_state_rate_area()
    final_lookup_and_output(plan_costs, zip_state_rate_area)


if __name__ == "__main__":
    main()
