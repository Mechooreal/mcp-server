from fastmcp import FastMCP
import requests
from dotenv import load_dotenv
import os
from korean_names import korean_names

load_dotenv()
API_KEY = os.getenv("API_KEY")

url = "http://apis.data.go.kr/1471000/FoodNtrCpntDbInfo02/getFoodNtrCpntDbInq02"

mcp = FastMCP(name="food_mcp_server", mask_error_details=True)

@mcp.tool(
    name= "getSearchFood",
    tags={"food", "search"},
    annotations={
        "title": "Search food nutrition facts",
        "openWorldHint": True
    }
)
def getSearchFood(
    FOOD_NM_KR: str = '',
    MAKER_NM: str = '',
    FOOD_CAT1_NM: str = '',
    DB_CLASS_NM: str = '품목대표',
    pageNo: int = 1, 
    numOfRows: int = 5
    ) -> list:
    """식품의약품안전처 식품영양성분DB에서 식품 정보를 검색합니다. 식품명, 업체명, 식품대분류명, 품목대표/상용제품 등을 기준으로 검색할 수 있습니다."""    
    params = {
        'serviceKey': API_KEY,
        'pageNo': pageNo,
        'numOfRows': numOfRows,
        'type': 'json', 
        'FOOD_NM_KR': FOOD_NM_KR,
        'MAKER_NM': MAKER_NM,
        'FOOD_CAT1_NM': FOOD_CAT1_NM,
        'DB_CLASS_NM': DB_CLASS_NM
    }
    print(params)
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        response_json = response.json()
        items = response_json.get("body", {}).get("items", [])
        transformed_data = []
        for item in items:
            new_item = {}
            for key, value in item.items():
                if value != '':
                    if key in korean_names:
                        new_item[korean_names[key]] = value
                    else:
                        new_item[key] = value 
            transformed_data.append(new_item)
        print(transformed_data)
        return transformed_data
    except requests.exceptions.RequestException as e:
        print(f"HTTP 요청 오류: {e}")
        return []

if __name__ == "__main__":
    mcp.run(
        transport="streamable-http", 
        path='/',
        port=19861
        )
