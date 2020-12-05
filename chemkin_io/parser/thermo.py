""" functions operating on the thermo block string
"""
import itertools
import numpy as np
import autoparse.pattern as app
import autoparse.find as apf
from ioformat import headlined_sections

COMMENTS_PATTERN = app.escape('!') + app.capturing(app.one_or_more(app.WILDCARD2))

def create_spc_nasa7_dct(block_str):
    """ Creates a spc_nasa7_dct


        :return spc_nasa7_dct: dictionary with spc names as keys and NASA-7 info as values

    """
    # Get the list of entries; at least four lines each (possibly more for comment lines)
    entry_lst = create_entry_list(block_str)
    
    # Get the default midpoint temp
    default_temp_limits = get_default_temp_limits(block_str)
    default_midpoint = default_temp_limits[1] 
    many_default_midpoints = list(itertools.repeat(default_midpoint, times=len(entry_lst)))  # creates an iterator
    
    # Get the spc names, which will be the keys of the dictionary
    spc_names = list(map(get_spc_name, entry_lst))

    # Get the NASA-7 parameters, which will be the values of the dictionary
    nasa7_params = list(
        zip(
            map(get_notes, entry_lst),
            map(get_composition, entry_lst),
            map(get_phase, entry_lst),
            map(get_temp_limits, entry_lst, many_default_midpoints),
            map(get_coeffs, entry_lst)
        )
    )

    spc_nasa7_dct = dict(zip(spc_names, nasa7_params))

    return spc_nasa7_dct


def create_entry_list(block_str, add_spaces=True):
    """ Creates a list with each line of the thermo block_str as an
        entry in that list
    
        :param block_str: string for thermo block

        :return line_lst: list of strs for each line

    """
    block_str = apf.remove(COMMENTS_PATTERN, block_str)
#    print('type of block_str\n', type(block_str))
    line_lst = list(apf.split_lines(block_str))
    #line_lst = list(block_str.splitlines)
#    print(type(line_lst))
    
    # Get the indices of the entry header lines
    header_idxs = []
    for idx, line in enumerate(line_lst):
        if len(line) >= 80 and line[79] == '1':
            header_idxs.append(idx)
    if not header_idxs:
        raise ImportError('No thermo headers in the file could be read. A "1" in column 80 marks this.')  
    header_idxs.append(len(line_lst))  # adds an entry to mark the end of the block_str
    
    # Check that there are at least 4 lines in each entry
    for idx, difference in enumerate(np.diff(header_idxs)):
        assert difference >= 4, (
            f'There are less than 4 lines for this thermo entry: \n{line_lst[header_idxs[idx]]}'
        )
    
    # Put together the thermo entries into a list of tuples
    entry_lst = []
    for idx in range(len(header_idxs)-1):  # skips the last entry
        entry = line_lst[header_idxs[idx]:header_idxs[idx+1]]
        entry_lst.append(entry)

    # Fix the problem of the missing spaces at the beginning of lines without negative signs
    entry_lst = fix_lines(entry_lst) 

    return entry_lst


def get_spc_name(entry, print_notice=False):
    """ Get the species name from the entry
        
        :param entry: the 4 or more lines making up the thermo entry
        :type entry: tuple
        :return spc_name: the name of the species, contained in the first 16 characters of the first line
        :rtype: str
    """
    first_line = entry[0]
    spc_name = first_line[0:16]  # first 16 characters
    spc_name = spc_name.split()[0]  # just get the first space-separated entry

    # If there's something other than a species name here, print a notice of this
    if len(spc_name) > 1 and print_notice:
        print('In the first 16 characters of the following line, there is something other than only a species name.')
        print('(These extra characters will not be saved)')
        print(f'{first_line}')

    return spc_name


def get_notes(entry):
    """ Get the misc notes from the first line of the entry. Note that this is technically for the date,
        but it can contain whatever information is so desired.
        
        :param entry: the 4 or more lines making up the thermo entry
        :type entry: tuple
        :return notes: the freeform notes from the first line of the entry
        :rtype: str
    """
    first_line = entry[0]
    notes = first_line[18:24]  # characters 19 through 24
    
    return notes


def get_composition(entry):
    """ Get the molecular composition information from the first line of the entry


        :return composition: a dictionary containing the molecular composition
        :rtype: dct {element: quantity, ...}

    """
    first_line = entry[0]
    full_comp_str = first_line[24:44]  # characters 25 through 44
    
    # Will add the ability to read the actual values later...for now, just return the str
    for idx in range(4):
        start = idx*5
        end = start + 5
        comp_str = full_comp_str[start:end]
        elem = comp_str[0:2]
        count = comp_str[2:5]
    
    composition = full_comp_str  # need to change later!

    # Also, there is room for a fifth entry right before the '1' on this line. Need to add this later.

    return composition
        

def get_temp_limits(entry, default_midpoint):
    """ Get the temperatures from the first line of the entry


        :return temp_limits
        :rtype: list[floats] [low_limit, high_limit, midpoint]  note the odd order
    """ 
    first_line = entry[0]
    formatted_entry = reform_entry(entry)  # for error printing
    full_temp_str = first_line[45:73]  # characters 46 through 73

    # Read the high and low limits
    try: 
        low_limit = float(first_line[45:55])  # characters 46 through 55 
        high_limit = float(first_line[55:65])  # characters 56 through 65
    except ValueError:
        print(f'Error processing the high and/or low temperatures in the following entry:\n{formatted_entry}')

    # If the midpoint read fails, replace it with the default value
    try:
        midpoint = float(first_line[65:73])  # characters 66 through 73
    except ValueError:
        midpoint = default_midpoint
        print(
            f'Using the default midpoint temperature, {default_midpoint}, for the following entry:\n{formatted_entry}'
        )

    temp_limits = [low_limit, high_limit, midpoint]

    return temp_limits


def get_phase(entry):
    """ Get the phase from the first line of the entry

        :return phase: 'G', 'L', or 'S'
        :rtype: str
    """ 
    first_line = entry[0]
    phase = first_line[44]  # character 45

    return phase


def get_coeffs(entry): 
    """ Get the NASA-7 polynomial coefficients from the last three lines of the entry

        :return coeffs: the two sets of 7 polynomial coefficients
        :rtype: tuple(lsts)  ([high_coeffs], [low_coeffs])
    """
    formatted_entry = reform_entry(entry)
    line_counter = 1
    for idx, line in enumerate(entry):
        
        # If on the first line or if the line is too short, skip the line
        if idx == 0 or len(line) < 80:
            continue
            
        # If on the second line of the actual thermo data
        if line_counter == 1:
            try:
                high_coeffs = list((float(line[0:15]), float(line[15:30]), float(line[30:45]),
                    float(line[45:60]), float(line[60:75])))
            except ValueError:
                print(f'Error reading values in line {idx+1} of the following entry:\n{formatted_entry}')
            line_counter += 1
                
        # If on the third line of the actual thermo data
        elif line_counter == 2:
            try:
                high_coeffs.extend(list((float(line[0:15]), float(line[15:30]))))
                low_coeffs = list((float(line[30:45]), float(line[45:60]), float(line[60:75])))
            except ValueError:
                print(f'Error reading values in line {idx + 1} of the following entry:\n{formatted_entry}')
            line_counter += 1
                
        # If on the fourth line of the actual thermo data
        elif line_counter == 3:
            try:
                low_coeffs.extend(list((float(line[0:15]), float(line[15:30]), float(line[30:45]),
                    float(line[45:60]))))
            except ValueError:
                print(f'Error reading values in line {idx + 1} of the following entry:\n{formatted_entry}')

    # Make sure three lines were read
    assert line_counter == 3, (
        f'Less than three lines of coefficients were read for the following entry:\n{formatted_entry}'
    )
    coeffs = tuple((high_coeffs, low_coeffs))

    return coeffs


def get_default_temp_limits(block_str):
    """ Gets the default temperatures from the header of a thermo block str

    """
    block_str = apf.remove(COMMENTS_PATTERN, block_str)
    line_lst = list(apf.split_lines(block_str))

    # Loop over each line
    for idx, line in enumerate(line_lst):
        try: 
            # Note that this order is different than that in the individual thermo entries
            low_limit = float(line[0:10])
            midpoint = float(line[10:20]) 
            high_limit = float(line[20:30]) 
            break
        except ValueError:
            pass
        # Check if the first thermo entry has been reached
        if len(line) >= 80 and line[79] == '1':
            raise ImportError(
                'No default temperature cutoffs could be found before the first thermo entry'
            )

    # Note that this order is different than that in the individual thermo entries
    default_temp_limits = [low_limit, midpoint, high_limit] 

    return default_temp_limits


def reform_entry(entry):
    """ Put the entry back together for error printing purposes

    """
    for idx, line in enumerate(entry):
        if idx == 0:
            formatted_entry = line
        else:
            formatted_entry += '\n' + line 

    return formatted_entry


def fix_lines(entry_lst):
    """ Because Python 2 is dumb and gets rid of leading whitespaces after a newline
    
    
    """
    for idx1, entry in enumerate(entry_lst):
        for idx2, line in enumerate(entry):
            if line:  # if the line is not empty
                first_char = line[0]
                if first_char.isdigit():  # for now, just check if the first character is a digit
                    line = ' ' + line
                    entry[idx2] = line
        entry_lst[idx1] = entry

    return entry_lst

    
# Functions which use thermo parsers to collate the data
def data_block(block_str):
    """ Parses all of the NASA polynomials in the species block of the
        mechanism file and subsequently pulls all of the species names
        and thermochemical properties.

        :param block_str: string for thermo block
        :type block_str: str
        :return data_block: all the data from the data string for each species
        :rtype: list(list(str/float))
    """

    thm_dstr_lst = data_strings(block_str)
    thm_dat_lst = tuple(zip(
        map(species_name, thm_dstr_lst),
        map(temperatures, thm_dstr_lst),
        map(low_coefficients, thm_dstr_lst),
        map(high_coefficients, thm_dstr_lst)))

    return thm_dat_lst


def data_dct(block_str, data_entry='strings'):
    """ Parse all of the NASA polynomials given in the thermo block
        of the mechanism input file and stores them in a dictionary.

        :param block_str: string for thermo block
        :type block_str: str
        :return therm_dct: all the data from the data string for each speices
        :rtype: dict[species: NASA polynomial string]
    """

    if data_entry == 'strings':
        thm_data_lst = data_strings(block_str)
        names = map(species_name, thm_data_lst)
        therm_dct = dict(zip(names, thm_data_lst))
    elif data_entry == 'block':
        thm_data_lst = data_block(block_str)
        print('inside chemkinio/parser/thermo.py, thm_data_lst\n', thm_data_lst)
        names = thm_data_lst[0]
        therm_dct = dict(zip(names, thm_data_lst))
    else:
        raise NotImplementedError

    return therm_dct


# Functions for parsing the thermo block or single polyn string #
def data_strings(block_str):
    """ Parse all of the NASA polynomials given in the thermo block
        of the mechanism input file and stores them in a list.

        :param block_str: string for thermo block
        :type block_str: str
        :return thm_strs: strings containing NASA polynomials for all species
        :rtype: list(str)
    """

    headline_pattern = (
        app.LINE_START + app.not_followed_by(app.one_of_these(
            [app.DIGIT, app.PLUS, app.escape('=')])) +
        app.one_or_more(app.NONNEWLINE) +
        app.escape('1') + app.LINE_END
    )
    thm_strs = headlined_sections(
        string=block_str.strip(),
        headline_pattern=headline_pattern
    )

    return thm_strs


def species_name(thm_dstr):
    """ Parses the name of the species from the NASA polynomial
        given in the data string for a species in the thermo block.

        :param thm_dstr: data string for species in thermo block
        :type thm_dstr: str
        :return name: name of the species
        :rtype: str
    """

    pattern = app.STRING_START + app.capturing(app.one_or_more(app.NONSPACE))
    name = apf.first_capture(pattern, thm_dstr)

    return name


def temperatures(thm_dstr):
    """ Parses the temperatures from the NASA polynomial
        given in the data string for a species in the thermo block.

        :param thm_dstr: data string for species in thermo block
        :type thm_dstr: str
        :return temps: temperatures (K)
        :rtype: tuple(float)
    """

    headline = apf.split_lines(thm_dstr)[0]
    pattern = (app.one_or_more(app.SPACE) + app.capturing(app.NUMBER) +
               app.one_or_more(app.SPACE) + app.capturing(app.NUMBER) +
               app.one_or_more(app.SPACE) + app.capturing(app.NUMBER) +
               app.one_or_more(app.SPACE) + app.DIGIT + app.STRING_END)
    captures = apf.first_capture(pattern, headline)
    assert captures, (
        f'No temperatures were captured for the datastring {thm_dstr}'
    )
    temps = tuple(map(float, captures))

    return temps


def low_coefficients(thm_dstr):
    """ Parses the low temperature coefficients from the NASA polynomial
        given in the data string for a species in the thermo block.

        :param thm_dstr: data string for species in thermo block
        :type thm_dstr: str
        :return cfts: low temperature coefficients
        :rtype: tuple(float)
    """

    capture_lst = apf.all_captures(app.EXPONENTIAL_FLOAT, thm_dstr)
    assert len(capture_lst) in (14, 15), (
        f'Number of captured terms is {len(capture_lst)}. Should be 14 or 15.'
        )
    cfts = tuple(map(float, capture_lst[7:14]))

    return cfts


def high_coefficients(thm_dstr):
    """ Parses the high temperature coefficients from the NASA polynomial
        given in the data string for a species in the thermo block.

        :param thm_dstr: data string for species in thermo block
        :type thm_dstr: str
        :return cfts: high temperature coefficients
        :rtype: tuple(float)
    """

    capture_lst = apf.all_captures(app.EXPONENTIAL_FLOAT, thm_dstr)
    assert len(capture_lst) in (14, 15)
    cfts = tuple(map(float, capture_lst[:7]))

    return cfts


def temp_common_default(block_str):
    """ Parses the common temperature defaults from the thermo block
        of the mechanism input file.

        :param block_str: string for thermo block
        :type block_str: str
        :return tmp_com_def: common temp defined in block
        :rtype: float
    """

    pattern = (app.UNSIGNED_FLOAT + app.LINESPACES +
               app.capturing(app.UNSIGNED_FLOAT) + app.LINESPACES +
               app.UNSIGNED_FLOAT)
    capture = apf.first_capture(pattern, block_str)
    assert capture
    tmp_com_def = float(capture)

    return tmp_com_def
