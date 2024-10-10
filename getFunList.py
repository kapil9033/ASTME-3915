#import re
#
#def step1(output_file):
#    with open(output_file, 'r') as file:
#        content = file.readlines()
#
#    searching_words = [line.strip() for line in content if line.startswith("SWC_Com_")]
#
#    with open('step1output.txt', 'w') as file:
#        for word in searching_words:
#            file.write(word + '\n')
#
#    return searching_words
#
#def step2(searching_words, tst_file):
#    with open(tst_file, 'r') as file:
#        content = file.readlines()
#
#    subprograms = {}
#    current_word = None
#    current_body = []
#
#    for line in content:
#        if line.startswith("-- Subprogram: "):
#            if current_word and current_body:
#                subprograms[current_word] = current_body
#            current_word = line.split(": ")[1].strip()
#            current_body = []
#        elif current_word in searching_words:
#            current_body.append(line)
#
#    if current_word and current_body:
#        subprograms[current_word] = current_body
#
#    with open('step2output.txt', 'w') as file:
#        for word, body in subprograms.items():
#            file.write(f"{word}:\n")
#            file.writelines(body)
#            file.write("\n")
#
#    return subprograms
#
#def step3_and_4(subprograms):
#    extracted_info = {}
#
#    for word, body in subprograms.items():
#        flow_body = []
#        in_flow = False
#
#        for i, line in enumerate(body):
#            if line.startswith("TEST.FLOW"):
#                in_flow = True
#                flow_body = []
#            elif line.startswith("TEST.END_FLOW"):
#                in_flow = False
#                if flow_body:
#                    first_line = flow_body[0]
#                    last_line = flow_body[-1]
#                    if first_line == last_line:
#                        if word not in extracted_info:
#                            extracted_info[word] = []
#                        extracted_info[word].append(flow_body[1:-1])
#            elif in_flow:
#                flow_body.append(line)
#
#    with open('step3output.txt', 'w') as file:
#        for word, flows in extracted_info.items():
#            file.write(f"{word}:\n")
#            for flow in flows:
#                file.writelines(flow)
#                file.write("\n")
#
#    return extracted_info
#
#def step5_and_6(extracted_info, searching_words, output_file):
#    prefixes = ["  ComWrapper.c.", "  Xlock.c.", "  DatasetVector_RteIf.c.", "  SWC_Com.c.","  SoftwareFilter.c.","  DatasetInfo.c."]
#
#    with open(output_file, 'r') as file:
#        content = file.readlines()
#
#    with open('funOutput.txt', 'w') as file:
#        for i, line in enumerate(content):
#            word = line.strip()
#            if word in extracted_info:
#                file.write(f"{word}\n")
#                for flow in extracted_info[word]:
#                    for flow_line in flow:
#                        # Step 6: Remove specified prefixes
#                        for prefix in prefixes:
#                            if flow_line.startswith(prefix):
#                                flow_line = flow_line[len(prefix):]
#                        file.write(flow_line)
#                    file.write("\n")
#            elif word in searching_words:
#                file.write(f"{word}\n")
#            else:
#                file.write('\n')
#
#    # Highlighting in output.txt
#    with open('highlighted_output.txt', 'w') as file:
#        for line in content:
#            for word in searching_words:
#                if word in line:
#                    line = line.replace(word, f"[HIGHLIGHT]{word}[/HIGHLIGHT]")
#            file.write(line)
#            
#def step7(output_file):
#    with open(output_file, 'r') as file:
#        content = file.readlines()
#
#    left_parts = []
#    current_part = []
#    in_part = False
#    line_number = 0
#
#    for i, line in enumerate(content):
#        if line.startswith("SWC_Com_"):
#            if current_part:
#                left_parts.append((current_part, line_number))
#            current_part = [line.strip()]
#            in_part = True
#            line_number = i + 1
#        elif in_part:
#            if line.strip() == "":
#                in_part = False
#            else:
#                current_part.append(line.strip())
#
#    if current_part:
#        left_parts.append((current_part, line_number))
#
#    return left_parts
#
#def step8(fun_output_file):
#    with open(fun_output_file, 'r') as file:
#        content = file.readlines()
#
#    right_major_parts = []
#    current_major_part = []
#    current_sub_part = []
#    in_major_part = False
#    in_sub_part = False
#    line_number = 0
#
#    for i, line in enumerate(content):
#        if line.startswith("SWC_Com_"):
#            if current_major_part:
#                right_major_parts.append((current_major_part, line_number))
#            current_major_part = [line.strip()]
#            current_sub_part = []
#            in_major_part = True
#            in_sub_part = True
#            line_number = i + 1
#        elif in_major_part:
#            if line.strip() == "":
#                if in_sub_part:
#                    current_major_part.append(current_sub_part)
#                    current_sub_part = []
#                    in_sub_part = False
#            else:
#                current_sub_part.append(line.strip())
#                in_sub_part = True
#
#    if current_major_part:
#        right_major_parts.append((current_major_part, line_number))
#
#    right_parts = []
#    for major_part, line_number in right_major_parts:
#        reserved_line = major_part[0]
#        for sub_part in major_part[1:]:
#            right_parts.append((reserved_line + "\n" + "\n".join(sub_part), line_number))
#
#    return right_parts
#
#def step9(left_parts, right_major_parts):
#    with open('Compare.txt', 'w') as file:
#        for left_index, (left_part, left_line_number) in enumerate(left_parts):
#            left_part_str = "\n".join(left_part)
#            matched = False
#
#            if left_index < len(right_major_parts):
#                right_major_part, right_line_number = right_major_parts[left_index]
#                for right_part in right_major_part:
#                    if left_part_str == right_part:
#                        matched = True
#                        break
#
#                if not matched:
#                    file.write(f"LEFT_PART (Line {left_line_number}):\n{left_part_str}\n\n")
#                    file.write(f"RIGHT_MAJOR_PART (Line {right_line_number}):\n{right_major_part}\n\n")
#            else:
#                # If there are more LEFT_PARTs than RIGHT_MAJOR_PARTs
#                file.write(f"LEFT_PART (Line {left_line_number}):\n{left_part_str}\n\n")
#                file.write("No corresponding RIGHT_MAJOR_PART found.\n\n")
#
#def main():
#    output_file = 'output.txt'
#    fun_output_file = 'funOutput.txt'
#
#    searching_words = step1(output_file)
#    subprograms = step2(searching_words, 'SWC_COM.tst')
#    extracted_info = step3_and_4(subprograms)
#    step5_and_6(extracted_info, searching_words, output_file)
#
#    left_parts = step7(output_file)
#    right_parts = step8(fun_output_file)
#    step9(left_parts, right_parts)
#
#
#if __name__ == "__main__":
#    main()
#

import re

def step1(output_file):
    with open(output_file, 'r') as file:
        content = file.readlines()

    searching_words = [line.strip() for line in content if line.startswith("SWC_Com_")]

    with open('step1output.txt', 'w') as file:
        for word in searching_words:
            file.write(word + '\n')

    return searching_words

def step2(searching_words, tst_file):
    with open(tst_file, 'r') as file:
        content = file.readlines()

    subprograms = {}
    current_word = None
    current_body = []

    for line in content:
        if line.startswith("-- Subprogram: "):
            if current_word and current_body:
                subprograms[current_word] = current_body
            current_word = line.split(": ")[1].strip()
            current_body = []
        elif current_word in searching_words:
            current_body.append(line)

    if current_word and current_body:
        subprograms[current_word] = current_body

    with open('step2output.txt', 'w') as file:
        for word, body in subprograms.items():
            file.write(f"{word}:\n")
            file.writelines(body)
            file.write("\n")

    return subprograms

def step3_and_4(subprograms):
    extracted_info = {}

    for word, body in subprograms.items():
        flow_body = []
        in_flow = False

        for i, line in enumerate(body):
            if line.startswith("TEST.FLOW"):
                in_flow = True
                flow_body = []
            elif line.startswith("TEST.END_FLOW"):
                in_flow = False
                if flow_body:
                    first_line = flow_body[0]
                    last_line = flow_body[-1]
                    if first_line == last_line:
                        if word not in extracted_info:
                            extracted_info[word] = []
                        extracted_info[word].append(flow_body[1:-1])
            elif in_flow:
                flow_body.append(line)

    with open('step3output.txt', 'w') as file:
        for word, flows in extracted_info.items():
            file.write(f"{word}:\n")
            for flow in flows:
                file.writelines(flow)
                file.write("\n")

    return extracted_info

def step5_and_6(extracted_info, searching_words, output_file):
    prefixes = ["  ComWrapper.c.", "  Xlock.c.", "  DatasetVector_RteIf.c.", "  SWC_Com.c.","  SoftwareFilter.c.","  DatasetInfo.c."]

    with open(output_file, 'r') as file:
        content = file.readlines()

    with open('funOutput.txt', 'w') as file:
        for i, line in enumerate(content):
            word = line.strip()
            if word in extracted_info:
                file.write(f"{word}\n")
                for flow in extracted_info[word]:
                    for flow_line in flow:
                        # Step 6: Remove specified prefixes
                        for prefix in prefixes:
                            if flow_line.startswith(prefix):
                                flow_line = flow_line[len(prefix):]
                        file.write(flow_line)
                    file.write("\n")
            elif word in searching_words:
                file.write(f"{word}\n")
            else:
                file.write('\n')

    # Highlighting in output.txt
    with open('highlighted_output.txt', 'w') as file:
        for line in content:
            for word in searching_words:
                if word in line:
                    line = line.replace(word, f"[HIGHLIGHT]{word}[/HIGHLIGHT]")
            file.write(line)
            
def step7(output_file):
    with open(output_file, 'r') as file:
        content = file.readlines()

    left_parts = []
    current_part = []
    in_part = False
    line_number = 0

    for i, line in enumerate(content):
        if line.startswith("SWC_Com_"):
            if current_part:
                left_parts.append((current_part, line_number))
            current_part = [line.strip()]
            in_part = True
            line_number = i + 1
        elif in_part:
            if line.strip() == "":
                in_part = False
            else:
                current_part.append(line.strip())

    if current_part:
        left_parts.append((current_part, line_number))

    return left_parts

def step8(fun_output_file):
    with open(fun_output_file, 'r') as file:
        content = file.readlines()

    right_major_parts = []
    current_major_part = []
    current_sub_part = []
    in_major_part = False
    in_sub_part = False
    line_number = 0

    for i, line in enumerate(content):
        if line.startswith("SWC_Com_"):
            if current_major_part:
                right_major_parts.append((current_major_part, line_number))
            current_major_part = [line.strip()]
            current_sub_part = []
            in_major_part = True
            in_sub_part = True
            line_number = i + 1
        elif in_major_part:
            if line.strip() == "":
                if in_sub_part:
                    current_major_part.append(current_sub_part)
                    current_sub_part = []
                    in_sub_part = False
            else:
                current_sub_part.append(line.strip())
                in_sub_part = True

    if current_major_part:
        right_major_parts.append((current_major_part, line_number))

    right_parts = []
    for major_part, line_number in right_major_parts:
        reserved_line = major_part[0]
        for sub_part in major_part[1:]:
            right_parts.append((reserved_line + "\n" + "\n".join(sub_part), line_number))

    return right_parts

def step9(left_parts, right_major_parts):
    with open('Compare.txt', 'w') as file:
        for left_index, (left_part, left_line_number) in enumerate(left_parts):
            left_part_str = "\n".join(left_part)
            matched = False

            if left_index < len(right_major_parts):
                right_major_part, right_line_number = right_major_parts[left_index]
                for right_part in right_major_part:
                    if left_part_str == right_part:
                        matched = True
                        break

                if not matched:
                    file.write(f"LEFT_PART (Line {left_line_number}):\n{left_part_str}\n\n")
                    file.write(f"RIGHT_MAJOR_PART (Line {right_line_number}):\n{right_major_part}\n\n")
            else:
                # If there are more LEFT_PARTs than RIGHT_MAJOR_PARTs
                file.write(f"LEFT_PART (Line {left_line_number}):\n{left_part_str}\n\n")
                file.write("No corresponding RIGHT_MAJOR_PART found.\n\n")


#def step9(left_parts, right_major_parts):
#    with open('Compare.txt', 'w') as file:
#        for left_index, (left_part, left_line_number) in enumerate(left_parts):
#            left_part_str = "\n".join(left_part)
#            matched = False
#
#            if left_index < len(right_major_parts):
#                right_major_part, right_line_number = right_major_parts[left_index]
#                for right_part in right_major_part:
##                   right_part_str = "\n".join(right_part)
#                    if left_part_str == right_part:
#                        matched = True
#                        break
#
#                if not matched:
#                    file.write(f"LEFT_PART (Line {left_line_number}):\n{left_part_str}\n\n")
#                    file.write(f"RIGHT_MAJOR_PART (Line {right_line_number}):\n")
#                    for right_part in right_major_part:
#                        right_part_str = "\n".join(right_part)
#                        file.write(f"{right_part_str}\n\n")
#            else:
#                # If there are more LEFT_PARTs than RIGHT_MAJOR_PARTs
#                file.write(f"LEFT_PART (Line {left_line_number}):\n{left_part_str}\n\n")
#                file.write("No corresponding RIGHT_MAJOR_PART found.\n\n")
                
def main():
    output_file = 'output.txt'
    fun_output_file = 'funOutput.txt'

    searching_words = step1(output_file)
    subprograms = step2(searching_words, 'SWC_COM.tst')
    extracted_info = step3_and_4(subprograms)
    step5_and_6(extracted_info, searching_words, output_file)

    left_parts = step7(output_file)
    right_parts = step8(fun_output_file)
    step9(left_parts, right_parts)


if __name__ == "__main__":
    main()








#import re
#
#def step1(output_file):
#    with open(output_file, 'r') as file:
#        content = file.readlines()
#
#    searching_words = [line.strip() for line in content if line.startswith("SWC_Com_")]
#
#    with open('step1output.txt', 'w') as file:
#        for word in searching_words:
#            file.write(word + '\n')
#
#    return searching_words
#
#def step2(searching_words, tst_file):
#    with open(tst_file, 'r') as file:
#        content = file.readlines()
#
#    subprograms = {}
#    current_word = None
#    current_body = []
#
#    for line in content:
#        if line.startswith("-- Subprogram: "):
#            if current_word and current_body:
#                subprograms[current_word] = current_body
#            current_word = line.split(": ")[1].strip()
#            current_body = []
#        elif current_word in searching_words:
#            current_body.append(line)
#
#    if current_word and current_body:
#        subprograms[current_word] = current_body
#
#    with open('step2output.txt', 'w') as file:
#        for word, body in subprograms.items():
#            file.write(f"{word}:\n")
#            file.writelines(body)
#            file.write("\n")
#
#    return subprograms
#
#def step3_and_4(subprograms):
#    extracted_info = {}
#
#    for word, body in subprograms.items():
#        flow_body = []
#        in_flow = False
#
#        for i, line in enumerate(body):
#            if line.startswith("TEST.FLOW"):
#                in_flow = True
#                flow_body = []
#            elif line.startswith("TEST.END_FLOW"):
#                in_flow = False
#                if flow_body:
#                    first_line = flow_body[0]
#                    last_line = flow_body[-1]
#                    if first_line == last_line:
#                        if word not in extracted_info:
#                            extracted_info[word] = []
#                        extracted_info[word].append(flow_body[1:-1])
#            elif in_flow:
#                flow_body.append(line)
#
#    with open('step3output.txt', 'w') as file:
#        for word, flows in extracted_info.items():
#            file.write(f"{word}:\n")
#            for flow in flows:
#                file.writelines(flow)
#                file.write("\n")
#
#    return extracted_info
#
#def step5(extracted_info, searching_words, output_file):
#    with open(output_file, 'r') as file:
#        content = file.readlines()
#
#    with open('funOutput.txt', 'w') as file:
#        for i, line in enumerate(content):
#            word = line.strip()
#            if word in extracted_info:
#                file.write(f"Line {i + 1} ({word}):\n")
#                for flow in extracted_info[word]:
#                    file.writelines(flow)
#                    file.write("\n")
#            elif word in searching_words:
#                file.write(f"Line {i + 1} ({word}): NOT FOUND in SWC_COM.tst\n")
#            else:
#                file.write('\n')
#
#    # Highlighting in output.txt
#    with open('highlighted_output.txt', 'w') as file:
#        for line in content:
#            for word in searching_words:
#                if word in line:
#                    line = line.replace(word, f"[HIGHLIGHT]{word}[/HIGHLIGHT]")
#            file.write(line)
#
#def main():
#    output_file = 'output.txt'
#    tst_file = 'SWC_COM.tst'
#
#    searching_words = step1(output_file)
#    subprograms = step2(searching_words, tst_file)
#    extracted_info = step3_and_4(subprograms)
#    step5(extracted_info, searching_words, output_file)
#
#if __name__ == "__main__":
#    main()