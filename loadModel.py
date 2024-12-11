import pandas as pd
from transformers import BertTokenizer, BertForSequenceClassification
import torch

# 저장된 모델 경로
model_path = "./trained_bert_model"

# 모델과 토크나이저 로드
model = BertForSequenceClassification.from_pretrained(model_path)
tokenizer = BertTokenizer.from_pretrained(model_path)

# 디바이스 설정 (GPU 사용 가능하면 GPU 사용, 그렇지 않으면 CPU 사용)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 모델을 디바이스로 이동
model = model.to(device)

# 모델을 평가 모드로 설정
model.eval()

# 예측할 데이터 로드
test_data_path = "./data/output.csv"
test_data = pd.read_csv(test_data_path)

# 입력 텍스트 생성
test_data["input_text"] = test_data.apply(
    lambda row: f"src_ip: {row['src_ip']}, dst_ip: {row['dst_ip']}, src_port: {row['src_port']}, dst_port: {row['dst_port']}, protocol: {row['protocol']}, payload: {row['payload']}", 
    axis=1
)

# 입력 텍스트를 리스트로 변환
input_texts = test_data["input_text"].tolist()

# 토큰화 및 텐서 변환
inputs = tokenizer(input_texts, return_tensors="pt", padding=True, truncation=True, max_length=128)

# 입력 데이터도 GPU로 이동
inputs = {key: val.to(device) for key, val in inputs.items()}

# 배치 크기 설정 (GPU 메모리 절약을 위해 배치 크기를 줄임)
batch_size = 8  # 배치 크기를 줄여서 메모리 사용량을 감소시킴
num_batches = len(inputs['input_ids']) // batch_size + 1

# 예측 수행 (배치 단위로 예측)
predictions = []
with torch.no_grad():
    for i in range(num_batches):
        batch_inputs = {key: val[i * batch_size: (i + 1) * batch_size].to(device) for key, val in inputs.items()}
        outputs = model(**batch_inputs)
        
        # 로짓(logits)을 소프트맥스 확률로 변환
        logits = outputs.logits
        probs = torch.softmax(logits, dim=1)
        
        # 가장 높은 확률의 클래스 예측
        batch_predictions = torch.argmax(probs, dim=1).cpu().numpy()
        predictions.extend(batch_predictions)

# 예측 결과 저장
test_data["predicted_label"] = predictions

label_map = {
    0: "Benign",
    1: "C&C",
    2: "Okiru",
    3: "HeartBeat",
    4: "PortScan",
    5: "DDoS"
}

# 예측된 숫자 라벨을 클래스 이름으로 변환
test_data["predicted_label_name"] = test_data["predicted_label"].map(label_map)

# print("예측 결과:", predictions)
df = pd.DataFrame(test_data)
csv_name = "./data/result.csv"
df.to_csv(csv_name, index=False)