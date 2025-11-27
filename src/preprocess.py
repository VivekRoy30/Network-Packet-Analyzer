import pandas as pd
import re

def extract_ports(info):
    match = re.match(r'(\d+)\s*>\s*(\d+)', info)
    if match:
        return int(match.group(1)), int(match.group(2))
    return 0, 0

def extract_flags(info):
    flags = {
        'SYN': 1,
        'ACK': 2,
        'FIN': 3,
        'RST': 4,
        'PSH': 5,
        'URG': 6,
        'Retransmission': 7,
        'Dup ACK': 8
    }
    for key in flags:
        if key in info:
            return flags[key]
    return 0

def preprocess(df):
    df = df.copy()

    # Compute Inter‑Arrival Time (IAT)
    df['Time'] = df['Time'].astype(float)
    df['iat'] = df['Time'].diff().fillna(0)

    # Parse ports + flags from Info column
    src_ports = []
    dst_ports = []
    flag_values = []

    for info in df['Info']:
        s, d = extract_ports(info)
        src_ports.append(s)
        dst_ports.append(d)
        flag_values.append(extract_flags(info))

    df['src_port'] = src_ports
    df['dst_port'] = dst_ports
    df['flags'] = flag_values

    # Encode protocol as integer
    df['protocol_enc'] = df['Protocol'].astype('category').cat.codes

    # Select final numeric ML features
    final = df[['Length', 'iat', 'src_port', 'dst_port', 'flags', 'protocol_enc']]

    return final.fillna(0)
