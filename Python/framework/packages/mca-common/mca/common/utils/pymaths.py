#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains math related classes and functions
The implementation is intended for simple math operations. If you need more advanced functionality use
mca.common.math3d classes.
"""

# mca python imports
import sys
import math
import struct
import random

# software specific imports

# mca python imports


AXIS = {'x': 0, 'y': 1, 'z': 2}
PI = math.pi
EPSILON = sys.float_info.epsilon                            # value used as a tolerance to compare float values.
MAX_INT = 2 ** (struct.Struct('i').size * 8 - 1) - 1        # maximum supported integer value by the system.


# =====================================================================================================================
# SCALAR
# =====================================================================================================================

def is_equal(x, y, tolerance=EPSILON):
    """
    Returns whether 2 float values are equal withing a given tolerance.

    :param float x: first float value to compare.
    :param float y: second float value to compare.
    :param float tolerance: comparison tolerance.
    :return: True if both float values can be considered equal; False otherwise.
    """

    return math.fabs(x - y) < sys.float_info.epsilon * math.fabs(
        x + y) * tolerance or math.fabs(x - y) < sys.float_info.epsilon


def lerp(start, end, alpha):
    """
    Computes a linear interpolation between two values.

    :param int or float start: start value to interpolate from.
    :param int or float end:  end value to interpolate to.
    :param int or float alpha: how far we want to interpolate (0=start, 1=end).
    :return: result of the linear interpolation.
    :rtype: float
    """

    return start + alpha * (end - start)
    # return (end * alpha) + ((1.0 - alpha) * start)


def clamp(number, min_value=0.0, max_value=1.0):
    """
    Clamps a number between two values.

    :param int or float number: numerical value to clamp.
    :param int or float min_value: maximum value of the number.
    :param int or float max_value: minimum value of the number.
    :return: clamped value.
    :return: int or float
    """

    return max(min(number, max_value), min_value)


def remap_value(value, old_min, old_max, new_min, new_max):
    """
    Remaps given value taking into consideration its old range and the new one.

    :param int or float value: numerical value to remap.
    :param int or float old_min: old minimum value of the value.
    :param int or float old_max: old minimum value of the value.
    :param int or float new_min: new minimum value of the value.
    :param int or float new_max: new minimum value of the value.
    :return: remapped value.
    :rtype: int or float
    """

    return new_min + (((value - old_min) * (new_max - new_min)) / (old_max - old_min))


def roundup(number, to):
    """
    Rounds up a number.

    :param int or float number: numerical value to roundup.
    :param int or float to: maximum value to roundup.
    :return: roundup value.
    :rtype: int or float
    """

    return int(math.ceil(number / to)) * to


def sign(value):
    """
    Returns the sign of the given value.

    :param int or float value: numerical value to retrieve sign of.
    :return: -1 of the value is negative; 1 if the value is positive; 0 if the value is zero.
    :rtype: int
    """

    return value and (1, -1)[value < 0]


def get_range_percentage(min_value, max_value, value):
    """
    Returns the percentage value along a line from min_vlaue to max_value that value is.

    :param int or float  min_value: minimum numerical value in range.
    :param int or float  max_value: maximum numerical value in range.
    :param int or float value: input value.
    :return: percentage (from 0.0 to 1.0) between the two values where input value is.
    :rtype: float
    """

    try:
        return (value - min_value) / (max_value - min_value)
    except ZeroDivisionError:
        return 0.0


def map_range_clamped(value, in_range_a, in_range_b, out_range_a, out_range_b):
    """
    Returns value mapped from one range into another where the value is clamped to the input range.
    For example, 0.5 normalized from the range 0:1 to 0:50 would result in 25.

    :param float value: numerical value to map clamp.
    :param int or float in_range_a: minimum numerical value in range before range clamping.
    :param int or float in_range_b: maximum numerical value in range before range clamping.
    :param int or float out_range_a: minimum numerical value that will be used by the linear interpolation.
    :param int or float out_range_b: maximum numerical value that will be used by the linear interpolation.
    :return: map clamp ranged value.
    :rtype: float
    """

    clamped_percentage = clamp(get_range_percentage(in_range_a, in_range_b, value), 0.0, 1.0)
    return lerp(out_range_a, out_range_b, clamped_percentage)


def map_range_unclamped(value, in_range_a, in_range_b, out_range_a, out_range_b):
    """
    Returns value mapped from one range into another where the value.
    For example, 0.5 normalized from the range 0:1 to 0:50 would result in 25.

    :param float value: numerical value to map clamp.
    :param int or float in_range_a: minimum numerical value in range before range.
    :param int or float in_range_b: maximum numerical value in range before range.
    :param int or float out_range_a: minimum numerical value that will be used by the linear interpolation.
    :param int or float out_range_b: maximum numerical value that will be used by the linear interpolation.
    :return: map ranged value.
    :rtype: float
    """

    clamped_percentage = get_range_percentage(in_range_a, in_range_b, value)
    return lerp(out_range_a, out_range_b, clamped_percentage)


def snap_value(value, base_value):
    """
    Returns snap value given an input and a base snap value.

    :param int or float value: numeric value to snap.
    :param int or float base_value: base snap value.
    :return: snapped value.
    :rtype: float
    """

    return round((float(value) / base_value)) * base_value


def fade_sine(percent_value):
    """
    fade sine by given percentage value.

    :param float percent_value: percent value to fade by.
    :return: fade sine value.
    :rtype: float
    """

    input_value = math.pi * percent_value

    return math.sin(input_value)


def fade_cosine(percent_value):
    """
    fade cosine by given percentage value.

    :param float percent_value: percent value to fade by.
    :return: fade cosine value.
    :rtype: float
    """

    percent_value = math.pi * percent_value

    return (1 - math.cos(percent_value)) * 0.5


def fade_smoothstep(percent_value):
    """
    fade smoothsetp by given percentage value.

    :param float percent_value: percent value to fade by.
    :return: fade smoothstep value.
    :rtype: float
    """

    return percent_value * percent_value * (3 - 2 * percent_value)


def fade_sigmoid(percent_value):
    """
    simple fade by given percentage value.

    :param float percent_value: percent value to fade by.
    :return: simple fade value.
    :rtype: float
    """

    if percent_value == 0:
        return 0

    if percent_value == 1:
        return 1

    input_value = percent_value * 10 + 1

    return (2 / (1 + (math.e**(-0.70258 * input_value)))) - 1


def ease_in_sine(percent_value):
    """
    ease in by given percentage value.

    :param float percent_value: percent value to ease in by.
    :return: ease in value.
    :rtype: float
    """

    return math.sin(1.5707963 * percent_value)


def ease_in_expo(percent_value):
    """
    ease in exponentially by given percentage value.

    :param float percent_value: percent value to ease in by.
    :return: ease in value.
    :rtype: float
    """

    return (pow(2, 8 * percent_value) - 1) / 255


def ease_out_expo(percent_value, power=2):
    """
    ease out exponentially by given percentage value.

    :param float percent_value: percent value to ease out by.
    :return: ease out value.
    :rtype: float
    """

    return 1 - pow(power, -8 * percent_value)


def ease_out_circ(percent_value):
    """
    ease out square root by given percentage value.

    :param float percent_value: percent value to ease out by.
    :return: ease out square root value.
    :rtype: float
    """

    return math.sqrt(percent_value)


def ease_out_back(percent_value):
    """
    ease out back by given percentage value.

    :param float percent_value: percent value to ease out by.
    :return: ease out back value.
    :rtype: float
    """

    return 1 + (--percent_value) * percent_value * (2.70158 * percent_value + 1.70158)


def ease_in_out_sine(percent_value):
    """
    sine ease int out by given percentage value.

    :param float percent_value: percent value to ease out by.
    :return: sine ease in out value.
    :rtype: float
    """

    return 0.5 * (1 + math.sin(math.pi * (percent_value - 0.5)))


def ease_in_out_quart(percent_value):
    """
    quart ease int out by given percentage value.

    :param float percent_value: percent value to ease out by.
    :return: quart ease in out value.
    :rtype: float
    """

    if percent_value < 0.5:
        percent_value *= percent_value
        return 8 * percent_value * percent_value
    else:
        percent_value -= 1
        percent_value *= percent_value
        return 1 - 8 * percent_value * percent_value


def ease_in_out_expo(percent_value):
    """
    ease int out exponentially by given percentage value.

    :param float percent_value: percent value to ease out by.
    :return: ease in out value.
    :rtype: float
    """

    if percent_value < 0.5:
        return (math.pow(2, 16 * percent_value) - 1) / 510
    else:
        return 1 - 0.5 * math.pow(2, -16 * (percent_value - 0.5))


def ease_in_out_circ(percent_value):
    """
    square root ease int out by given percentage value.

    :param float percent_value: percent value to ease out by.
    :return: square root ease in out value.
    :rtype: float
    """

    if percent_value < 0.5:
        return (1 - math.sqrt(1 - 2 * percent_value)) * 0.5
    else:
        return (1 + math.sqrt(2 * percent_value - 1)) * 0.5


def ease_in_out_back(percent_value):
    """
    ease int out back by given percentage value.

    :param float percent_value: percent value to ease out by.
    :return: ease in out back value.
    :rtype: float
    """

    if percent_value < 0.5:
        return percent_value * percent_value * (7 * percent_value - 2.5) * 2
    else:
        return 1 + (percent_value - 1) * percent_value * 2 * (7 * percent_value + 2.5)


def average_position(pos1=(0.0, 0.0, 0.0), pos2=(0.0, 0.0, 0.0), weight=0.5):
    """
    Returns the average of the two given positions. You can weight between 0 (first input) or 1 (second_input).

    :param tuple(float, float, float) pos1: first input position.
    :param tuple(float, float, float) pos2: second input position.
    :param float weight: amount to weight between the two input positions.
    :return: average position.
    :rtype: tuple(float, float, float)
    """

    return (
        pos1[0] + ((pos2[0] - pos1[0]) * weight),
        pos1[1] + ((pos2[1] - pos1[1]) * weight),
        pos1[2] + ((pos2[2] - pos1[2]) * weight)
    )


def smooth_step(value, range_start=0.0, range_end=1.0, smooth=1.0):
    """
    Interpolates between 2 float values using hermite interpolation.

    :param float value: value to smooth.
    :param float range_start: minimum value of interpolation range.
    :param float range_end: maximum value of interpolation range.
    :param float smooth: strength of the smooth applied to the value.
    :return: interpoalted value.
    :rtype: float
    """

    # normalized value
    range_val = range_end - range_start
    normalized_val = value / range_val

    # smooth value
    smooth_val = pow(normalized_val, 2) * (3 - (normalized_val * 2))
    smooth_val = normalized_val + ((smooth_val - normalized_val) * smooth)
    value = range_start + (range_val * smooth_val)

    return value


def distribute_value(samples, spacing=1.0, range_start=0.0, range_end=1.0):
    """
    Returns a list of values distributed between a start and end range.

    :param int samples: number of values to sample across the value range.
    :param float spacing: incremental scale for each sample distance.
    :param float range_start: minimum value in the sample range.
    :param float range_end: maximum value in the sample range.
    :return: distributed values in range.
    :rtype: List(float)
    """

    # Get value range
    value_list = [range_start]
    value_dst = abs(range_end - range_start)
    unit = 1.0

    # Find unit distance
    factor = 1.0
    for i in range(samples - 2):
        unit += factor * spacing
        factor *= spacing
    unit = value_dst / unit
    total_unit = unit

    # Build Sample list
    for i in range(samples - 2):
        mult_factor = total_unit / value_dst
        value_list.append(range_start - ((range_start - range_end) * mult_factor))
        unit *= spacing
        total_unit += unit

    # Append final sample
    value_list.append(range_end)

    return value_list


def inverse_distance_weight_1d(value_array, sample_value, value_domain=(0, 1), cycle_value=False):
    """
    Returns the inverse distance weight for a given sample point given an array of scalar values.

    :param list(float) value_array: value array to calculate weights from.
    :param float sample_value: float, sample point to calculate weights for.
    :param tuple(float) or list(float) value_domain: minimum and maximum range of the value array.
    :param bool cycle_value: whether to calculate or not the distance based on a closed loop of values.
    :return: inverse distance weight.
    :rtype: float
    """

    dst_array = list()
    total_inv_dst = 0.0

    # Calculate inverse distance weight
    for v in range(len(value_array)):
        dst = abs(sample_value - value_array[v])
        if cycle_value:
            value_domain_len = value_domain[1] - value_domain[0]
            f_cyc_dst = abs(sample_value - (value_array[v] + value_domain_len))
            r_cyc_dst = abs(sample_value - (value_array[v] - value_domain_len))
            if f_cyc_dst < dst:
                dst = f_cyc_dst
            if r_cyc_dst < dst:
                dst = r_cyc_dst

        # Check zero distance
        if dst < 0.00001:
            dst = 0.00001

        dst_array.append(dst)
        total_inv_dst += 1.0 / dst

    # Normalize value weights
    weight_array = [(1.0 / d) / total_inv_dst for d in dst_array]

    return weight_array


def max_index(numbers):
    """
    Returns the largest number in the given list of numbers.

    :param list(int) or list(float) or list(str) numbers: list of numbers to get maximum value of.
    :return: maximum value from given list of numbers.
    :rtype: int or float or str
    """

    max_value = 0
    result = 0
    for i in numbers:
        current_value = abs(float(i))
        if current_value > max_value:
            max_value = current_value
            result = numbers.index(i)

    return result


def mean_value(numbers):
    """
    Returns the mean/average value of the given numbers.

    :param list[int or float] numbers: list of numbers.
    :return: mean/average value.
    :rtype: int or float
    """

    return float(sum(numbers)) / max(len(numbers), 1)


def find_vector_length(v1):
    """
    For a given vector find the length

    :param [float|int] v1: The vector to check lengths against.
    :return: The total length of the given vector.
    :rtype: float
    """
    return math.sqrt(round(sum([x * x for x in v1]), 5))


def find_midpoint_between_points(pt1, pt2):
    """
    For two given points find the point between them.

    :param list[float|int] pt1: The first point in space
    :param list[float|int] pt2: The second point in space
    :return: A list containing of the final position.
    :rtype list[float|int]
    """
    return add_vectors(pt2, scale_vector(sub_vectors(pt1, pt2), .5))


def find_distance_between_points(pt1, pt2):
    """
    For two given points find the distance between them.

    :param list[float|int] pt1: The first point in space
    :param list[float|int] pt2: The second point in space
    :return: A list containing of the final position.
    :rtype list[float|int]
    """
    return find_vector_length(sub_vectors(pt2, pt1))


def normalize_vector(v1):
    """
    Given a vector normalize the values such the total venctor length is 1.

    :param list[float|int] v1: The vector to be normalized.
    :return: The normalized vector.
    :rtype: list[float|int]
    """
    length = find_vector_length(v1)
    return [round(x / length, 5) for x in v1]


def find_cross_product(v1, v2):
    """
    Given two vectors find the cross product between them.

    :param list[float|int] v1: The first vector.
    :param list[float|int] v2: The second vector.
    :return: A list representing the cross product.
    :rtype: list[float|int]
    """
    v_size = len(v1)
    return [round(v1[(index + 1) % v_size] * v2[(index + 2) % v_size] - v1[(index + 2) % v_size] * v2[(index + 1) % v_size], 5) for index in range(v_size)]


def add_vectors(v1, v2):
    """
    For two vector values return a final vector that is the sum of both.

    :param list[float|int] v1: The first vector.
    :param list[float|int] v2: The second vector.
    :return: A list representing the final vector value
    :rtype: list[float|int]
    """
    return [round(a + b, 5) for a, b in zip(v1, v2)]


def sub_vectors(v1, v2):
    """
    For two vector values return a final vector that is the difference of both.

    :param list[float|int] v1: The first vector.
    :param list[float|int] v2: The second vector.
    :return: A list representing the final vector value
    :rtype: list[float|int]
    """
    return [round(a - b, 5) for a, b in zip(v1, v2)]


def average_vectors(v_list):
    """
    From a list of vector values find the average of a sum of all magnitudes.

    :param list[list[float|int]] v_list: A list of vectors.
    :return: A vector the represents the average of all passed vector magnitudes.
    :rtype: list[float|int]
    """
    base_v = v_list[0]
    for vec in v_list[1:]:
        base_v = add_vectors(base_v, vec)
    return scale_vector(base_v, 1.00/len(v_list))


def scale_vector(v1, sca):
    """
    From a given vector scale all of its magnitudes by a value.

    :param list[float|int] v1: A given vector
    :param float sca: A value to scale the vector by.
    :return: The modified vector values
    :rtype: list[float|int]
    """
    return [round(v*sca, 5) for v in v1]


def create_random_list(min_max=None, length=None, int_only=False):
    """
    Creates a list of random numbers.

    :param list(float,float) min_max:
    :param int length: Length of the list desired.
    :param bool int_only: If the values should be ints only.
    :return: A list of random numeric values.
    :rtype: list[number]
    """
    min_max = min_max or (0, 1)
    length = length or 3
    if int_only:
        return [random.randint([round(x) for x in min_max]) for n in range(length)]
    else:
        return [random.uniform(*min_max) for n in range(length)]