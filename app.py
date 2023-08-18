import streamlit as st
import pandas as pd
import plotly.express as px
import os
import datetime
import openpyxl

## 기초

st.set_page_config(page_title="메리츠 매니저 Summer Event 대시보드",page_icon="📊",layout='wide', initial_sidebar_state='expanded')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)




### 여기부터는 햄버거 메뉴 없애는 곳들

hide_streamlit_style = """
            <style>
            MainMenu {visibility: hidden;}
            # [data-testid="collapsedControl"] {
            #     display: none
            }
            footer {visibility: hidden;}
             a:link {
                text-decoration: none;
            }

            a:visited {
                text-decoration: none;
            }

            a:hover {
                text-decoration: none;
            }

            a:active {
                text-decoration: none;
            }

            img {
            width: 100%; /* takes the 100 % width of its container (.box div)*/
            height: 100%; /* takes the 100 % height of its container (.box div)*/
            # border : 1;
            }


            </style>
            """

st.markdown(hide_streamlit_style, unsafe_allow_html=True) 






### 베이스파일


file_name = r'rawdata.xlsx'


### 데이터프레임 읽기


@st.cache_data
def find_excelfile_mod_date():
    time1 = os.path.getmtime(file_name)
    time2 = datetime.datetime.fromtimestamp(time1)
    return time2


@st.cache_data
def read_df():
    return pd.read_excel(file_name, skiprows=6, sheet_name='SM,AM 시상')
df = read_df()

@st.cache_data
def read_df_TOP300_300():
    return pd.read_excel(file_name, skiprows=3, sheet_name='TOP300_300만')
df_TOP300_300 = read_df_TOP300_300()


@st.cache_data
def read_df_TOP300_500():
    return pd.read_excel(file_name, skiprows=3, sheet_name='TOP300_500만')

df_TOP300_500 = read_df_TOP300_500()


@st.cache_data
def read_df_TOP300_700():
    return pd.read_excel(file_name, skiprows=3, sheet_name='TOP300_700만')

df_TOP300_700 = read_df_TOP300_700()


@st.cache_data
def read_df_gr_300():
    return pd.read_excel(file_name, skiprows=3, sheet_name='순증_300만')

df_순증_300 = read_df_gr_300()


@st.cache_data
def read_df_gr_500():
    return pd.read_excel(file_name, skiprows=3, sheet_name='순증_500만')

df_순증_500 = read_df_gr_500()


@st.cache_data
def read_df_gr_700():
    return pd.read_excel(file_name, skiprows=3, sheet_name='순증_700만')

df_순증_700 = read_df_gr_700()



@st.cache_data
def read_cell_value():
    wb = openpyxl.load_workbook(file_name,read_only=True)
    sb = wb['SM,AM 시상']
    return str(sb['a3'].value)
close_date = read_cell_value()




df.rename(columns = {'타겟\n목표' : '타겟목표'}, inplace = True)
df.rename(columns = {'매핑\n실적' : '매핑실적'}, inplace = True)
df.rename(columns = {' 사번' : '사번'}, inplace = True)
df.rename(columns = {'MC인원.1' : 'MC인원'}, inplace = True)


df_TOP300_300.rename(columns = {'타겟\n목표' : '타겟목표'}, inplace = True)
df_TOP300_300.rename(columns = {'매핑\n실적' : '매핑실적'}, inplace = True)
df_TOP300_300.rename(columns = {' 사번' : '사번'}, inplace = True)


df_TOP300_500.rename(columns = {'타겟\n목표' : '타겟목표'}, inplace = True)
df_TOP300_500.rename(columns = {'매핑\n실적' : '매핑실적'}, inplace = True)
df_TOP300_500.rename(columns = {' 사번' : '사번'}, inplace = True)



df_TOP300_700.rename(columns = {'타겟\n목표' : '타겟목표'}, inplace = True)
df_TOP300_700.rename(columns = {'매핑\n실적' : '매핑실적'}, inplace = True)
df_TOP300_700.rename(columns = {' 사번' : '사번'}, inplace = True)




df_순증_300.rename(columns = {'타겟\n목표' : '타겟목표'}, inplace = True)
df_순증_300.rename(columns = {'매핑\n실적' : '매핑실적'}, inplace = True)
df_순증_300.rename(columns = {' 사번' : '사번'}, inplace = True)

df_순증_500.rename(columns = {'타겟\n목표' : '타겟목표'}, inplace = True)
df_순증_500.rename(columns = {'매핑\n실적' : '매핑실적'}, inplace = True)
df_순증_500.rename(columns = {' 사번' : '사번'}, inplace = True)


df_순증_700.rename(columns = {'타겟\n목표' : '타겟목표'}, inplace = True)
df_순증_700.rename(columns = {'매핑\n실적' : '매핑실적'}, inplace = True)
df_순증_700.rename(columns = {' 사번' : '사번'}, inplace = True)



df['타겟목표'] = df['타겟목표'].apply(lambda x : 99999999 if x==0 else x)
# df['calc_달성률'] = (df['매핑실적']/df['타겟목표']*100).round(decimals=3)

# df['calc_순위'] = df['calc_달성률'].rank(ascending=False).fillna(999).astype(int)


st.sidebar.header('Dashboard `version 1`')

st.sidebar.subheader('Meritz Summer Event')

조건_지점명 = st.sidebar.selectbox('지점선택', df['지점'].unique().tolist()) 


옵션_매니저명 = df[~(df['타겟목표']==99999999) & (df['지점']==조건_지점명)].매니저.unique().tolist()



조건_매니저명 = st.sidebar.selectbox('매니저명 선택', 옵션_매니저명
                             ) 

조건_타겟목표 = df[(df['지점']==조건_지점명) & (df['매니저']==조건_매니저명)].타겟목표.values[0]
조건_매니저사번 = df[(df['지점']==조건_지점명) & (df['매니저']==조건_매니저명)].사번.values[0]


with st.sidebar:
    # close_date = str(20230801)
    st.markdown("---")
    st.write("데이터업데이트")
    st.write(find_excelfile_mod_date())

    st.markdown("---")
    with st.sidebar.expander("데이터 업데이트(관리자만)"):
        passwd = st.text_input("데이터관리비밀번호")
        if passwd == '7958':
            if st.button("새로고침하기"):
                # Clears all st.cache_resource caches:
                st.cache_data.clear()

            datafile = st.file_uploader("파일을 업로드해주세요",type=['xlsx'])
                        
            def save_uploadedfile(uploadedfile):
                with open('rawdata.xlsx',"wb") as f:
                    f.write(uploadedfile.getbuffer())
                #  return st.success("File saved")


            if datafile is not None:
                file_details = {"FileName":datafile.name,"FileType":datafile.type}
                save_uploadedfile(datafile)



    st.markdown("---")




def return_progress_df(타겟목표):
    if 5000000>타겟목표 >=3000000:
        return df_TOP300_300
    elif 7000000>타겟목표 >=5000000:
        return df_TOP300_500
    elif 타겟목표 >7000000:
        return df_TOP300_700
    else:
        return False
 
def return_progress_rank(타겟목표):
    if 5000000>타겟목표 >=3000000:
        return 90
    elif 7000000>타겟목표 >=5000000:
        return 120
    elif 타겟목표 >7000000:
        return 90
    else:
        return 0

def return_progress_gubun(타겟목표):
    if 5000000>타겟목표 >=3000000:
        return "300만"
    elif 7000000>타겟목표 >=5000000:
        return "500만"
    elif 타겟목표 >7000000:
        return "700만"
    else:
        return "기타"



def return_gr_df(타겟목표):
    if 5000000>타겟목표 >=3000000:
        return df_순증_300
    elif 7000000>타겟목표 >=5000000:
        return df_순증_500
    elif 타겟목표 >7000000:
        return df_순증_700
    else:
        return False


def return_gr_rank(타겟목표):
    if 5000000>타겟목표 >=3000000:
        return 60
    elif 7000000>타겟목표 >=5000000:
        return 80
    elif 타겟목표 >7000000:
        return 60
    else:
        return 0




# Row  



시상순위한도 = return_progress_rank(조건_타겟목표)
구간 = return_progress_gubun(조건_타겟목표)
profile = 조건_지점명 + " | " + 조건_매니저명  + " | " + "시상구간 : "+ 구간

st.markdown(f'### Meritz Summer Event 진행사항  :{close_date}')
st.markdown(f'{profile}')

st.markdown("---")
st.markdown("#####  Key Numbers")

# Row1
col1, col2, col3, col4 = st.columns(4)

# Row1-1

df_1 = return_progress_df(조건_타겟목표)

def return_values_from_df_top(df, 조건_매니저사번):
    타겟목표 = df[df['사번']==조건_매니저사번].타겟목표.values[0]
    매핑실적 = df[df['사번']==조건_매니저사번].매핑실적.values[0]
    달성률 = df[df['사번']==조건_매니저사번].달성률.values[0] +0.00001
    순위 = df[df['사번']==조건_매니저사번].순위.values[0]

    df.sort_values('달성률', ascending=False, inplace=True)
    순위_달성률 = df.iloc[시상순위한도-1]['달성률']

    return 타겟목표, 매핑실적, 달성률, 순위_달성률, 순위


## 순위달성률 = 90등 60등 시상대상의 순위임
타겟목표, 매핑실적, 달성률, 순위_달성률, 순위 = return_values_from_df_top(df_1,조건_매니저사번)

# Row1-2 매니저 순위
col1.metric('Top300', str(순위)+" 위", str(시상순위한도-순위)+"위", delta_color="inverse")
col1.caption(f'목표{구간}↑ {시상순위한도}위 대비')


col2.metric(f"목표진척률", str(round(달성률*100,1))+"%",str(round((달성률-순위_달성률)*100,1))+' %p*',delta_color="inverse")
col2.caption(f"*현재 {시상순위한도}위 매니저 대비")


# Row1-3 MC목표대비 달성률


def retrun_MC_from_df(df, 조건_매니저사번):
    MC인원 = df[df['사번']==조건_매니저사번].MC인원.iloc[0,1]
    MC목표 = df[df['사번']==조건_매니저사번].MC목표.iloc[0]
    return MC인원, MC목표

MC인원, MC목표 = retrun_MC_from_df(df,조건_매니저사번)

col3.metric(f"MC진척", str(MC인원)+"명",str(round((MC인원-MC목표),1))+' 명*',delta_color="inverse")
col3.caption(f"*목표 {MC목표}명 대비")



# Row1-4 순증률 진척사항



df_2 = return_gr_df(조건_타겟목표)
순증시상순위한도 = return_gr_rank(조건_타겟목표)



def return_values_from_df_순증(df, 조건_매니저사번):
    순증률 = df[df['사번']==조건_매니저사번].순증률.values[0]
    df['직전2개월'] = (df['6월실적'] + df['7월실적'])/2

    직전2개월 = df[df['사번']==조건_매니저사번].직전2개월.values[0]
    순증순위 = df[df['사번']==조건_매니저사번].순위.values[0]
    df.sort_values('순증률', ascending=False, inplace=True)
    시상제한순위_순증률 = df.iloc[순증시상순위한도-1]['순증률']


    return 순증률, 직전2개월, 순증순위, 시상제한순위_순증률


순증률, 직전2개월, 순증순위, 시상제한순위_순증률 = return_values_from_df_순증(df_2,조건_매니저사번)


col4.metric("순증률순위", str(순증순위)+"위", str(순증시상순위한도-순증순위)+'위', delta_color="inverse")
col4.caption(f"*{순증시상순위한도}위 대비, 순증률{(round(순증률*100)):,}%")

# st.markdown("---")

과부족금액 = int((조건_타겟목표*(달성률-순위_달성률))/10000)*-1
if 과부족금액>0:
    과부족멘트 = "부족합니다"
else:
    과부족멘트 = "초과합니다"


순증_과부족금액 = int((직전2개월*(순증률-시상제한순위_순증률))/10000)*-1
if 순증_과부족금액>0:
    순증_과부족멘트 = "부족합니다"
else:
    순증_과부족멘트 = "초과합니다"


cola1, cola2, cola3 = st.columns([2,8,2])
with cola2:
    st.markdown("")
    st.error(f'######  	☑️ :red[Top300 시상] 순위권 {시상순위한도}위 까지 :red[{abs(과부족금액)}만원] {과부족멘트} ')
    st.error(f'###### 	☑️ :blue[순증시상] 순위권 {순증시상순위한도}위 까지 :blue[{abs(순증_과부족금액)}만원] {순증_과부족멘트}')

st.markdown("---")



### 차트만들기
### 
### 차트만들기 - 진척률 순위표




df_chart_base = return_progress_df(조건_타겟목표)
df_chart_base['매니저명'] = df_chart_base.apply(lambda x : str(x['순위'])+"_"+x['매니저'], axis=1)
df_chart_base['달성률'] = df_chart_base['달성률']*100


def find_topBottom(chart_range):
    if 순위-chart_range<0:
        chart_start, chart_end = 0, chart_range-1
    else:
        chart_start, chart_end = 순위-int(chart_range/2), 순위+int(chart_range/2)
    return chart_start, chart_end



st.markdown("##### TOP300 진척현황")

colc1, colc2 = st.columns([2,8])

with colc1:
    chart_options = [50,100,len(df_chart_base)]
    chart_range = st.selectbox("최대 표시갯수",chart_options,len(chart_options)-1)


chart_start, chart_end = find_topBottom(chart_range)

#표시갯수에 따라서 그릴 차트를 정리함
df_chart1 = df_chart_base.iloc[chart_start:chart_end].copy()


chart_max = df_chart1['달성률'].max()
chart_min = df_chart1[df_chart1['달성률']>2]['달성률'].min()



highlighted_bar = df_chart1[df_chart1['사번']==조건_매니저사번].매니저명.values[0]
highlighted_bar_지점 = df_chart1[df_chart1['지점']==조건_지점명].매니저명.values.tolist()



fig = px.bar(df_chart1,
             x='매니저명',
             y = '달성률',
             template = 'simple_white',
             range_y =[chart_min,chart_max]
            )



fig.update_traces(
    marker_color=['blue' if x in highlighted_bar_지점 else 'grey' for x in df_chart1['매니저명']],
                #   else 'grey' for x in df_chart1['매니저명']],  
# Blue for 'Clothing', grey for others
    textposition='inside'  # Position the text inside the bars
)



# # Find the sales value for 'Clothing'
highlighted_bar_sales = df_chart1.loc[df_chart1['매니저명'] == highlighted_bar, '달성률'].values[0]


# Add annotation for the highlighted bar
fig.add_annotation(
    x=highlighted_bar, y=highlighted_bar_sales,  # Coordinates for the annotation
    text=조건_매니저명,  # Text to display
    showarrow=True,  # Use arrow or not
    font=dict(size=15, color="white"),  # Font settings
    bgcolor="blue",  # Background color
    opacity=0.8  # Opacity
)


fig.update_yaxes(visible=True, showticklabels=True, )

st.plotly_chart(fig, use_container_width=True)




st.markdown("##### 순증시상 진척현황")

df_chart_base2 = return_gr_df(조건_타겟목표)
df_chart_base2['매니저명'] = df_chart_base2.apply(lambda x : str(x['순위'])+"_"+x['매니저'], axis=1)
df_chart_base2['순증률'] = df_chart_base2['순증률']*100



def find_topBottom2(chart_range):
    if 순증순위-chart_range<0:
        chart_start, chart_end = 0, chart_range-1
    else:
        chart_start, chart_end = 순증순위-int(chart_range/2), 순증순위+int(chart_range/2)
    return chart_start, chart_end



chart_start, chart_end = find_topBottom2(chart_range)

#표시갯수에 따라서 그릴 차트를 정리함
df_chart2 = df_chart_base2.iloc[chart_start:chart_end].copy()


chart_max2 = df_chart2['순증률'].max()
chart_min2 = df_chart2['순증률'].min()


highlighted_bar = df_chart2[df_chart2['사번']==조건_매니저사번].매니저명.values[0]
highlighted_bar_지점 = df_chart2[df_chart2['지점']==조건_지점명].매니저명.values.tolist()

fig = px.bar(df_chart2,
             x='매니저명',
             y = '순증률',
             template = 'simple_white',
             range_y =[chart_min2,chart_max2]
            )



fig.update_traces(
    marker_color=['blue' if x in highlighted_bar_지점 else 'grey' for x in df_chart2['매니저명']],
                #   else 'grey' for x in df_chart1['매니저명']],  
# Blue for 'Clothing', grey for others
    textposition='inside'  # Position the text inside the bars
)


                                                                     
# # Find the sales value for 'Clothing'
highlighted_bar_sales = df_chart2.loc[df_chart2['매니저명'] == highlighted_bar, '순증률'].values[0]


# Add annotation for the highlighted bar
fig.add_annotation(
    x=highlighted_bar, y=highlighted_bar_sales,  # Coordinates for the annotation
    text=조건_매니저명,  # Text to display
    showarrow=True,  # Use arrow or not
    font=dict(size=15, color="white"),  # Font settings
    bgcolor="blue",  # Background color
    opacity=0.8  # Opacity
)


fig.update_yaxes(visible=True, showticklabels=True, )

st.plotly_chart(fig, use_container_width=True)
