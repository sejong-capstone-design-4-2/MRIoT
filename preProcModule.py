import subprocess
import json
import pandas as pd
import re

# PCAP 파일 경로와 출력 JSON 파일 경로
pcap_file = "./data/dump.pcap"
output_json = "./data/output.json"

# tshark 명령어
cmd = ["tshark", "-r", pcap_file, "-T", "json"]

# JSON 파일로 저장
with open(output_json, "w") as output_file:
    subprocess.run(cmd, stdout=output_file)

print(f"JSON 파일이 생성되었습니다: {output_json}")

# JSON 데이터 로드 (UTF-8 인코딩 및 에러 대체 처리)
json_path = "./data/"
json_name = "output"
with open(json_path + json_name + ".json", encoding="utf-8", errors="replace") as f:
    data = json.load(f)

# JSON 데이터에서 필요한 필드 추출
records = []
for item in data:
    try:
        source = item["_source"]["layers"]

        # 프레임 시간 가져오기 및 비 ASCII 문자 제거
        #frame_time = source["frame"].get("frame.time", "")
        #frame_time = re.sub(r"[^\x00-\x7F]+", "", frame_time)  # 비 ASCII 문자 제거

        # 공통 필드 (TCP 및 UDP)
        record = {
            #"frame_time": frame_time.strip(),
            "src_mac": source["eth"].get("eth.src", "") if "eth" in source else "",
            "dst_mac": source["eth"].get("eth.dst", "") if "eth" in source else "",
            "src_ip": source["ip"].get("ip.src", "") if "ip" in source else "",
            "dst_ip": source["ip"].get("ip.dst", "") if "ip" in source else "",
            "protocol": source["frame"].get("frame.protocols", ""),
            "transport_protocol": "",
            "src_port": "",  # TCP 또는 UDP에서 채워질 예정
            "dst_port": "",  # TCP 또는 UDP에서 채워질 예정
            "payload": ""    # TCP 또는 UDP에서 채워질 예정
        }

        # TCP 및 UDP에 따라 필드 채우기
        if "tcp" in source:
            record["transport_protocol"] = "TCP"  # 추가된 필드
            record["src_port"] = source["tcp"].get("tcp.srcport", "")
            record["dst_port"] = source["tcp"].get("tcp.dstport", "")
            record["payload"] = source["tcp"].get("tcp.payload", "")
        elif "udp" in source:
            record["transport_protocol"] = "UDP"  # 추가된 필드
            record["src_port"] = source["udp"].get("udp.srcport", "")
            record["dst_port"] = source["udp"].get("udp.dstport", "")
            record["payload"] = source["udp"].get("udp.payload", "")

        records.append(record)
    except KeyError as e:
        print(f"Missing key: {e}")

# DataFrame으로 변환 및 CSV 파일 저장
df = pd.DataFrame(records)
csv_name = "./data/" + json_name + ".csv"
df.to_csv(csv_name, index=False)

print("CSV 파일이 생성되었습니다: ", csv_name)