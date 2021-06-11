""" Importing math and sys modules """
import math
import sys

def find_median(input_list):
    """Function to find medain to the given input list sort the input list and find length,
    check whether the length is odd or even and find median"""
    input_list.sort()
    count = len(input_list)
    if count % 2 == 0:
        median1 = input_list[count // 2]
        median2 = input_list[count // 2 - 1]
        median = (median1 + median2) / 2
    else:
        median = input_list[count // 2]
    return median


def find_variance(input_list, avg):
    """ Finding variance by using the formula by using the average """
    var = 0
    count = len(input_list)
    try:
        for val in input_list:
            var = var + ((val - avg) ** 2)
        return var / (count - 1)
    except ZeroDivisionError:
        return 0

def find_standard_deviation(val):
    """ Finding SD by using square root function to variance """
    return math.sqrt(val)


def find_average(input_list):
    """ Finding average sum of input numbers divided by length of input list"""
    return sum(input_list)/len(input_list)

def main():
    """ main """
    count = 0
    valid_num_count = 0
    numbers = []
    file_name = sys.argv[1] #giving input file name
    column_to_parse = int(sys.argv[2]) #giving column number
    with open(file_name, 'r') as infile: #opening the input file in read mode
        for line in infile:
            try:
                col_val = float(line.split()[column_to_parse])
                if math.isnan(col_val): #checking whether the value is NaN or not
                    count = count+1
                else:
                    count = count+1
                    valid_num_count = valid_num_count+1
                    numbers.append(col_val) #appending value to the list called numbers
            except IndexError:
                temp = "Exiting: There is no valid 'list index' in column {} in line {} in file :{}"
                print(temp.format(column_to_parse, (count+1), file_name))
                sys.exit()
            except ValueError:
                count = count+1
                temp = "Skipping line number {} : could not convert string to float : {}"
                print(temp.format(count, (line.split()[column_to_parse])))
    if valid_num_count == 0:
        temp = "Error: There were no valid number(s) in column {} in file: {}"
        print(temp.format(column_to_parse, file_name))
    else:
        #calling all functions and performing stats
        average = find_average(numbers)
        maximum = max(numbers)
        minimum = min(numbers)
        variance = find_variance(numbers, average)
        standard_deviation = find_standard_deviation(variance)
        median = find_median(numbers)
        print("\t{:<4} {}".format("Column:", column_to_parse))
        print("\n")
        #printing all the values using .format()
        print("\t\t{:<9} {} {:>10.3f}".format("Count", "=", count))
        print("\t\t{:<9} {} {:>10.3f}".format("ValidNum", "=", valid_num_count))
        print("\t\t{:<9} {} {:>10.3f}".format("Average", "=", average))
        print("\t\t{:<9} {} {:>10.3f}".format("Maximum", "=", maximum))
        print("\t\t{:<9} {} {:>10.3f}".format("Minimum", "=", minimum))
        print("\t\t{:<9} {} {:>10.3f}".format("Variance", "=", variance))
        print("\t\t{:<9} {} {:>10.3f}".format("Std Dev", "=", standard_deviation))
        print("\t\t{:<9} {} {:>10.3f}".format("Median", "=", median))
if __name__ == '__main__':
    main()
