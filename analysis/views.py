from __future__ import division
from email import contentmanager
import json
from operator import ge
from django.http import JsonResponse
from django.shortcuts import render

from pydantic import Json
import joblib
import csv
from django.db.models import Q






from analysis.models import Locate_Info, realty_data, full_data_model

# Create your views here.

first_quarter = []
second_quarter = []
third_quarter = []
fourth_quarter = []


def gu_search(request,gu_name) :
  print(gu_name)
  loc_datas = Locate_Info.objects.filter( 
        Q(gu__icontains=gu_name)
    )
  context = {
        'loc_datas':loc_datas,
        'loc_datas_js':json.dumps([ loc_data.to_json() for loc_data in loc_datas ])
    
  }
  print(loc_datas)

  return render(request,'analysis/gu_loc_datas.html',context)

def analysis_select(request) :
  return render(request,"analysis/analysis-select.html")


def analysis_result(request) :

    # print(type(prediction))
    if request.method == 'POST' :

      

      datas = request.POST

      categort1_1 = datas.get('category2')

      gu = convert_gu(datas.get('gu'))
      budget = datas.get('budget')
      category1 = datas.get('category1')
      category2 = convert_category2(datas.get('category2'))
      gender = convert_gender(datas.get('gender'))
      weekOrWeeken = convert_weekOrWeeken(datas.get('week-weeken')) 
      dayOrNight = convert_dayOrNight(datas.get('day-night')) 
      age_category = convert_age_category(datas.get('age-category')) 

      first_quarter = get_division_data(2021,1,datas.get('gu'),category2)
      second_quarter = get_division_data(2021,2,datas.get('gu'),category2)
      third_quarter = get_division_data(2021,3,datas.get('gu'),category2)
      fourth_quarter = get_division_data(2021,4,datas.get('gu'),category2)

      print(category2)

      # 데이터 구하기 위한 부분 
      season_profit = 0 
      season_count = 0
      for data in fourth_quarter :
        season_profit += data.season_profit
        season_count  += data.season_count
      season_count /= len(fourth_quarter)
      season_profit /= len(fourth_quarter)

      # 분기당 점포수 데이터 
      store_count = [len(first_quarter),len(second_quarter),len(third_quarter),len(fourth_quarter)]
      store_count_label = ["22-1","22-2","22-3","22-4"]  
      print("분기당 점포수 데이터",store_count)

      # 분기당 점포 매출 건수
      store_sell_count_data = []
      store_sell_count_data_label = ["22-1","22-2","22-3","22-4"]
      temp = 0
      for data in first_quarter :
        temp += data.season_count
      store_sell_count_data.append(temp)
      temp = 0
      for data in second_quarter : 
        temp += data.season_count
      store_sell_count_data.append(temp)
      temp = 0
      for data in third_quarter : 
        temp += data.season_count
      store_sell_count_data.append(temp)
      temp = 0
      for data in fourth_quarter : 
        temp += data.season_count
      store_sell_count_data.append(temp)
      print("분기당 매출 건수 :  ", store_sell_count_data)


      # 업종 분포 
      sector_list = {
        "외식업":["분식전문점","양식음식점","일식음식점","제과점","중식음식점","치킨전문점","커피-음료","패스트푸드점","한식음식점","호프-간이주점"],
        "교육":["문구","서적","스포츠강습","예술학원","완구","국어학원","일반교습학원"],
        "의료":["의료기기","의약품","일반의원","치과의원","한의원"],
        "식자재":["미곡판매","반찬가게","수산물판매","슈퍼마켓","육류판매","청과상","편의점"],
        "취미":["PC방","골프연습장","네일숍","노래방","당구장","미용실","피부관리실","화장품"],
        "생활용품":["세탁소","안경","여관","자동차미용","자동차수리","철물점"],
        "가전":["가전제품","가전제품수리","컴퓨터및주변장치판매","핸드폰"],
        "스포츠":["스포츠클럽","운동/경기용품","자전거 및기타 운송장비"],
        "의류":["가방","섬유제품","시계및귀금속","신발","일반의류"],
        "기타":["가구","고시원","부동산중개업","애완동물","인테리어","전자상거래업","조명용품","화초"]
      }
      candi_sector = sector_list[category1]
      sector_data = [0,0]
      sector_data_label = [datas.get('category2'),category1]
      for data in fourth_quarter :
        if data.service_name == categort1_1 :
          sector_data[0] += 1 
        elif data.service_name in candi_sector : 
          sector_data[1] +=1 
      

      # 주중 주말
      week_weeken_data = [0,0]
      week_weeken_data_label = ["주중","주말"]
      for data in fourth_quarter : 
        week_weeken_data[0] += data.week_count
        week_weeken_data[1] += data.weeken_count
      # week_weeken_data[0] = int(week_weeken_data[0]/sum(week_weeken_data)*100)
      # week_weeken_data[1] = 100-week_weeken_data[0]

      # 낮/ 밤 
      day_night_data = [0,0]
      day_night_data_label = ["낮","밤"]
      for data in fourth_quarter : 
        day_night_data[0] += data.day_count
        day_night_data[1] += data.night_count
      # day_night_data[0] = int(day_night_data[0]/sum(day_night_data)*100)
      # day_night_data[1] = 100-day_night_data[0]

      # 성별 
      male_female_data = [0,0]
      male_female_label = ["남","여"]
      for data in fourth_quarter : 
        male_female_data[0] += data.male_count
        male_female_data[1] += data.female_count
      # male_female_data[0] = int(male_female_data[0]/sum(male_female_data)*100)
      # male_female_data[1] = 100-male_female_data[0]

      # 연령대별 
      young_youth_elder_old_data = [0,0,0,0]
      young_youth_elder_old_data_label = ['청년(10대)','청소년(2,30대)','장년(40대)','중장년(50대이상)']
      for data in fourth_quarter : 
        young_youth_elder_old_data[0] += data.young_count
        young_youth_elder_old_data[1] += data.youth_count
        young_youth_elder_old_data[2] += data.elder_count
        young_youth_elder_old_data[3] += data.old_count
      sum_data = sum(young_youth_elder_old_data)
      # young_youth_elder_old_data[0] = int(young_youth_elder_old_data[0]/sum_data*100)
      # young_youth_elder_old_data[1] = int(young_youth_elder_old_data[1]/sum_data*100)
      # young_youth_elder_old_data[2] = int(young_youth_elder_old_data[2]/sum_data*100)
      # young_youth_elder_old_data[3] = 100-sum(young_youth_elder_old_data[:3])

      print("구분별 :" , sector_data)
      print("주중 주말 : ",week_weeken_data)
      print("낮 밤 : ", day_night_data)
      print("성별 : ", male_female_data)
      print("연령대별 : ", young_youth_elder_old_data)

      input_data = [2021] + [4,gu,category2] + [season_profit,season_count] + weekOrWeeken + dayOrNight + gender + age_category
      predicted_dong = analysis(gu,[input_data])[0]


      realty_datas = realty_data.objects.filter(
        Q(dong=predicted_dong) &
        Q(deposit__lte=int(budget))
      ).order_by("-deposit")[:10]

      loc_datas = []

      loc_info_datas = Locate_Info.objects.filter(
        Q(dong=predicted_dong)
      )

      for loc_info_data in loc_info_datas :
        lat = loc_info_data.latitude
        lon = loc_info_data.longitude
        name = loc_info_data.name
        loc_datas.append([lat,lon])
      print(loc_datas)

      # prediction = analysis(1,[[2021,4,4,9,213120599,3134,31,70,101,0,65,35,0,0,12,88]])

      # 전 분기 매출금액, 매출건수 
      former_divison_profit_count = [0,0]
      for data in fourth_quarter : 
        former_divison_profit_count[0] += data.season_profit
        former_divison_profit_count[1] += data.season_count

      print(loc_datas)

      context = {
        'predicted_dong' : predicted_dong,
        'store_count' : store_count,
        "store_count_label" :  json.dumps(store_count_label),
        'store_sell_count_data' : store_sell_count_data,
        'store_sell_count_data_label' : store_sell_count_data_label,
        'sector_data' : sector_data,
        'sector_data_label' : sector_data_label,
        'week_weeken_data' : week_weeken_data,
        'week_weeken_data_label' : week_weeken_data_label,
        'day_night_data' : day_night_data,
        'day_night_data_label' : day_night_data_label,
        'male_female_data' : male_female_data,
        'male_female_label' : male_female_label,
        'young_youth_elder_old_data' : young_youth_elder_old_data,
        'young_youth_elder_old_data_label' : young_youth_elder_old_data_label,
        'realty_datas' : realty_datas,
        'loc_datas' : loc_datas,
        # 'loc_datas_tojs' : [ loc_data.to_json() for loc_data in loc_datas],
        'former_divison_profit' : former_divison_profit_count[0],
        'former_divison_count' : former_divison_profit_count[1],
        'category1' : category1,
        'categort1_1' : categort1_1
      }

      return render(request,"analysis/analysis-result.html",context)
    
    return render(request,"analysis/analysis-result.html")

def get_division_data(year,season,gu,category1) :
  full_datas = full_data_model.objects.filter(
      Q(year=year) &
      Q(season=season) &
      Q(gu=gu)&
      Q(service=category1)
  )
  return full_datas

def convert_age_category(age) :
  if age == "청소년" :
    return [40,20,20,20]
  elif age == "청년" : 
    return [20,40,20,20]
  elif age == "장년" :
    return [20,20,40,20]
  elif age == "중장년" :
    return [20,20,20,40]
  else :
    return [33,33,33,33]


def convert_gender(gender) : 
  if gender == "남" :
    return [70,30]
  elif gender == "여" : 
    return [30,70] 
  else : 
    return [50,50]

def convert_weekOrWeeken(date) :
  if date == "주중" : 
    return [70,30]
  elif date == "주말" :
    return [30,70] 
  else :
    return [50,50]

def convert_dayOrNight(day) :
  if day == "낮" :
    return [70,30]
  elif day == "밤" :
    return [30,70] 
  else : 
    return [50,50]

def convert_gu(gu) :

  if gu == "양천구" or gu == "강서구" :
    return 0 
  elif gu == "영등포구" :
    return 1 
  elif gu == "구로구" or gu == "금천구" or gu == "동작구" or gu == "관악구" :
    return 2 
  elif gu == "서초구" :
    return 3 
  elif gu == "강남구" :
    return 4 
  elif gu == "송파구" or gu == "강동구" :
    return 5
  elif gu == "성동구" or gu == "광진구" or gu == "동대문구" or gu == "중랑구" : 
    return 6
  elif gu == "성북구" or gu == "강북구" or gu == "도봉구" or gu == "노원구" :
    return 7
  elif gu == "은평구" or gu == "서대문구" :
    return 8
  elif gu == "종로구" :
    return 9
  elif gu == "중구" :
    return 10
  elif gu == "용산구" or gu == "마포구" :
    return 11


def convert_category2(category2) :

  if  category2 == "분식전문점" or category2 == "양식음식점" or category2 == "일식음식점" or category2 == "제과점" or category2 == "중식음식점" or category2 == "치킨전문점" or category2 == "커피-음료" or category2 == "패스트푸드점" or category2 == "한식음식점" or category2 == "호프-간이주점" :
    return 0
  elif category2 == "문구" or category2 == "서적" or category2 == "스포츠강습" or category2 == "예술학원" or category2 == "완구" or category2 == "국어학원" or category2 == "일반교습학원" :
    return 1
  elif category2 == "의료기기" or category2 == "의약품" or category2 == "일반의원" or category2 == "치과의원" or category2 == "한의원" :
    return 2 
  elif category2 == "미곡판매" or category2 == "반찬가게" or category2 == "수산물판매" or category2 == "슈퍼마켓" or category2 == "육류판매" or category2 == "청과상" or category2 == "편의점" :
    return 3 
  elif category2 == "PC방" or category2 == "골프연습장" or category2 == "네일숍" or category2 == "노래방" or category2 == "당구장" or category2 == "미용실" or category2 == "피부관리실" or category2 == "화장품" :
    return 4
  elif category2 == "세탁소" or category2 == "안경" or category2 == "여관" or category2 == "자동차미용" or category2 == "자동차수리" or category2 == "철물점" :
    return 5
  elif category2 == "가전제품" or category2 == "가전제품수리" or category2 == "컴퓨터및주변장치판매" or category2 == "핸드폰" :
    return 6
  elif category2 == "스포츠클럽" or category2 == "운동/경기용품" or category2 == "자전거 및기타 운송장비" :
    return 7
  elif category2 == "가방" or category2 == "섬유제품" or category2 == "시계및귀금속" or category2 == "신발" or category2 == "일반의류" :
    return 8
  elif category2 == "가구" or category2 == "고시원" or category2 == "부동산중개업" or category2 == "애완동물" or category2 == "인테리어" or category2 == "전자상거래업" or category2 == "조명용품" or category2 == "화초" : 
    return 9
  else :
    return 4


def analysis(part, datas=[[2021,4,4,9,213120599,3134,31,70,101,0,65,35,0,0,12,88]]) :

  if part == 0 :
    model = joblib.load(f"/Users/hong/Desktop/KB It's your academy/predict_model/rf_{0}.pkl")  # path 값 설정해줘야 0~ 11
    return model.predict(datas)
  elif part == 1 :
    model = joblib.load(f"/Users/hong/Desktop/KB It's your academy/predict_model/rf_{1}.pkl")
    return model.predict(datas)
  elif part == 2 :
    model = joblib.load(f"/Users/hong/Desktop/KB It's your academy/predict_model/rf_{2}.pkl")
    return model.predict(datas)
  elif part == 3 : 
    model = joblib.load(f"/Users/hong/Desktop/KB It's your academy/predict_model/rf_{3}.pkl")
    return model.predict(datas)

  elif part == 4 :
    model = joblib.load(f"/Users/hong/Desktop/KB It's your academy/predict_model/rf_{4}.pkl")
    return model.predict(datas) 

  elif part == 5 : 
    model = joblib.load(f"/Users/hong/Desktop/KB It's your academy/predict_model/rf_{5}.pkl")
    return model.predict(datas)

  elif part == 6 :
    model = joblib.load(f"/Users/hong/Desktop/KB It's your academy/predict_model/rf_{6}.pkl")
    return model.predict(datas)

  elif part == 7 :
    model = joblib.load(f"/Users/hong/Desktop/KB It's your academy/predict_model/rf_{7}.pkl")
    return model.predict(datas)
  
  elif part == 8 :
    model = joblib.load(f"/Users/hong/Desktop/KB It's your academy/predict_model/rf_{8}.pkl")
    return model.predict(datas)

  elif part == 9 :
    model = joblib.load(f"/Users/hong/Desktop/KB It's your academy/predict_model/rf_{9}.pkl")
    return model.predict(datas)

  elif part == 10 :
    model = joblib.load(f"/Users/hong/Desktop/KB It's your academy/predict_model/rf_{10}.pkl")
    return model.predict(datas)

  elif part == 11 : 
    model = joblib.load(f"/Users/hong/Desktop/KB It's your academy/predict_model/rf_{11}.pkl")
    return model.predict(datas)


# def pre_input(gu = 0, category1 = 0,분기금액 = 0,분기건수 = 0,주중 = True,주말 = False,낮 = True,밤 = False,남 = True,여 = False,청소년 = True,청년 = False,장년 = False,중노년 = False) :
#   분기금액 = df.loc[(df['기준년코드'] == 2021) & (df['기준분기코드'] ==4) & (df['지역분류'] == gu) & (df['서비스분류'] == category1), '분기당매출금액'].mean()
#   분기건수 = df.loc[(df['기준년코드'] == 2021) & (df['기준분기코드'] ==4) & (df['지역분류'] == gu) & (df['서비스분류'] == category1), '분기당매출건수'].mean()
#   pre_list = [2021,4,gu, category1,분기금액, 분기건수, 주중, 주말, 낮, 밤, 남, 여, 청소년, 청년, 장년, 중노년]
#   for i in range(6,12) : 
#     if pre_list[i] == True :
#       pre_list[i] *= 70
#     if pre_list[i] == False : 
#       pre_list[i] = (pre_list[i] + 1) * 30
#   for i in range(12,16) : 
#     if pre_list[i] == True :
#       pre_list[i] *= 55
#     if pre_list[i] == False : 
#       pre_list[i] = (pre_list[i] + 1) * 15
#   return np.array(pre_list).reshape(1,-1)s


def read_csv() :
  path = "/Users/hong/Desktop/KB It's your academy/상권구역2.csv"
  file = open(path)
  reader = csv.reader(file) 

  for row in reader : 
    date_data, division, name, longitude, latitude, city, gu, dong = row 
    Loc_form = Locate_Info(
      data_date = date_data, division = division, name = name, 
      longitude = longitude, latitude = latitude, city = city, gu = gu, dong = dong
    )
    try : 
      Loc_form.save()
    except : 
      print("Loc Form error")


def read_full_data_of_csv() :

  path = "/Users/hong/Desktop/KB It's your academy/full_data_TRAS_final.csv"
  file = open(path)
  reader = csv.reader(file)
  idx = 0 
  for row in reader :
    if idx ==0 :
      idx = 1 
      continue
    index ,year, season, local, dump, service, service_name, season_profit, season_count, week_rate, weeken_rate, week_count, weeken_count, day_count, night_count, day_rate,night_rate, young_count, youth_count, elder_count, old_count,young_rate, youth_rate, elder_rate, old_rate, male_rate, female_rate,male_count,female_count,gu,dong = row 
    week_count, weeken_count,day_count, night_count,young_count,youth_count,elder_count,old_count,male_count,female_count = int(float(week_count)), int(float(weeken_count)), int(float(day_count)), int(float(night_count)), int(float(young_count)), int(float(youth_count)), int(float(elder_count)), int(float(old_count)), int(float(male_count)),int(float(female_count))
    data_form = full_data_model(idx=index,
      year=year, season=season, local=local, service=service, service_name=service_name, season_profit=season_profit,season_count=season_count,
      week_rate=week_rate,week_count=week_count, weeken_rate=weeken_rate, weeken_count=weeken_count, male_rate=male_rate,
      male_count=male_count, female_rate=female_rate, female_count=female_count,day_rate=day_rate,day_count=day_count,
      night_rate=night_rate, night_count=night_count,young_rate=young_count, young_count=young_count,youth_rate=youth_rate, 
      youth_count=youth_count ,elder_rate=elder_rate, elder_count=elder_count, old_rate=old_rate, old_count=old_count, 
      gu=gu, dong=dong
    )
    try :
      data_form.save()
      print(row)
    except :
      print("form_update_error")



def update_data(request) : 
  # read_csv()
  # read_full_data_of_csv()
  # read_reality()

  # datas = full_data_model.objects.all()
  # datas.delete()

  return render(request,"analysis/update-data.html") 


def read_reality() :
  path = "/Users/hong/Desktop/KB It's your academy/realty.csv"
  file = open(path)
  reader = csv.reader(file)
  for row in reader : 
    idx, bd_type1, bd_type2, city, gu, dong, name, trade_type,  deposit, month_price, leasable_area, total_area, floor, total_floor, direction, detail= row 
    realty_model = realty_data(
      idx=idx, bd_type1=bd_type1, bd_type2=bd_type2, city=city, gu=gu, dong=dong, name=name, trade_type=trade_type,
      deposit=deposit, month_price=month_price, leasable_area=leasable_area, total_area=total_area, floor=floor,
      total_floor=total_floor, direction=direction, detail=detail
    )
    try : 
      realty_model.save()
      print(row)
    except :
      print("realty data input error")



gu_list = {
  "신사동":[37.523733,127.022437],"논현동":[37.513788,127.031059],"삼성동":[37.512987, 127.053322],"강일동":[37.564718, 127.175237],
  "상일동":[37.549957,127.165259],"고덕동":[37.560499,127.156849],"명일동":[37.550098,127.146491],"암사동":[37.555917,127.129913],
  "천호동":[37.541298,127.124280],"길동":[37.537440,127.145959],"번동":[37.635614,127.033352],"수유동":[37.640679,127.016821],
  "우이동":[37.663180,127.012513],"염창동":[37.554020,126.873098],"등촌동":[37.560604,126.848496],"내발산동":[37.549998,126.819231],
  "가양동":[37.568483,126.841133],"마곡동":[37.572555,126.831406],"외발산동":[37.547174,126.820990],"공항동":[37.561363,126.795135],
  "과해동":[37.565474,126.787864],"오곡동":[37.554015,126.787271],"방화동":[37.573189,126.810872],"개화동":[37.570128,126.812975],
  "능동":[37.554073,127.083604],"구의동":[37.550163,127.091146],"광장동":[37.545713,127.102081],"화양동":[37.541823,127.071699],
  "가리봉동":[37.481358,126.888250],"개봉동":[37.493535,126.856247], "오류동":[37.489391,126.837243], "항동":[37.479989,126.822536],
  "온수동":[37.479989,126.822536],"궁동":[37.479989,126.822536],"중계동":[37.650570,127.076792],"쌍문동":[37.649180,127.027125],
  "방학동":[37.665259,127.042892],"창동":[37.647461,127.044105],"도봉동":[37.686979,127.041289],"신설동":[37.575347,127.025230],
  "용두동":[37.575439,127.035480],"평동":[37.568125,126.966642],
}