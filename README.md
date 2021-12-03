# fetch_dataset
데이터셋 새로 구하는 코드 정리 완료


# 사용법
## 1. 코랩 접속
- !git clone https://github.com/kangmyoungseok/fetch_dataset.git 입력
- fetch_dataset 폴더가 다운받아지면, 해당 폴더 안에 있던 main.py, Labeling_v3.1.csv, lib폴더 밖의 경로로 빼기

![image](https://user-images.githubusercontent.com/33647663/144436389-52affa49-2ed8-453f-b7a1-2ab28f5aeee6.png)


## 2. __구글 드라이브 꼭!!!!!!!!!!! 연결하기__ 
- 확인 세번하기.. 꼭꼭꼭

![image](https://user-images.githubusercontent.com/33647663/144436794-f8824b43-ea81-4769-8dd9-a8e71451f819.png)


## 3. !python3 main.py 입력해서 실행
- 나 : 1번, 유진: 2번, 유나: 3번, 승우: 4번

![image](https://user-images.githubusercontent.com/33647663/144437097-f8161e6a-b1f3-4b58-914a-f4e00f7b6a7c.png)


# 4. F12 들어가서 colab 안꺼지게 하는 코드 입력
    
    function ClickConnect(){
    console.log("코랩 연결 끊김 방지"); 
    document.querySelector("#star-icon").click()}

    setInterval(ClickConnect, 60 * 1000)

# 5. PC 전원 안꺼지게 하는건 당연한거 알죠?
![image](https://user-images.githubusercontent.com/33647663/144437838-4c3d7aeb-c93c-4659-b1d4-537c54b0f1b3.png)

# 나눠서 잘 돌려보자구 !

# 6. merge.py 
- 나눠서 구한 Labeling 파일 하나로 병합 -> Labeling_v3.3.csv

# 7. Labeling_to_Dataset.py
- Labeling 파일을 Dataset 형태로 변환 -> Dataset_v1.9.csv
- 수작업으로 Dataset_v1.9.csv에서 각 컬럼별로 정렬해서 상위 몇개 값이 튀는 애들 삭제. 총 30개 정도?

# 8. validate.py
- False로 라벨링 된 토큰중에 혹시,, 스캠이 발생한 애들이 있는지. 16개 발견해서 True로 라벨링 변경
- -> Dataset_v1.10.csv -> Web Application에서 사용할 최종 데이터셋 Fix
