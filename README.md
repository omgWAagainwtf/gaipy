# Gaipy 
Gaipy為NUDB的python版API，提供8個常用function，方便使用者進行資料庫操作
## 資料型態
* text
    * 文字，資料庫內會自動斷詞
    * 可使用Search function做全文索引搜尋
* num
    * 數字
* time
    * 時間
    * 依時序排序使用
* date
    * 日期
## 回傳格式
* res
    * Type: bool
    * 回傳是否執行成功
* msg
    * Type: str
    * 成功或錯誤資訊
* data
    * Type: dict or list of dict
    * 資料庫回傳內容
## 函式介紹
* **Create(db, args, wieghted column)**
    * 功能: 新建一個新的資料庫
    * db: 
        * Type: str
        * 屬性: **必填**
        * 說明: 要建立的DB名稱
    * args:
        * Type: dict
        * 屬性: **必填**
        * 說明: {'欄位名稱','資料型態'}
    * wieghted column:
        * Type: list
        * 屬性: 選填
        * 說明: args裡面的欄位加權，影響最終搜尋輸出時的排序分數
    * Usage:
        ```
        DB = 'all_col_no_weight'
        create_arg = {'title':'text','content':'text','post_time':'time','post_date':'date','likes':'num'}
        weighted_col = ['title','content']
        gp.Create(DB, create_arg, weighted_col)
        ```        
* **Insert(db, record, record_format, rb)**
    * 功能: 插入單/多筆資料
    * db:
        * Type: str
        * 屬性: **必填**
        * 說明: 要建立的DB名稱
    * record:
        * Type: str, dict or list of dict
        * 屬性: **必填**
        * 說明: 要插入的資料
    * record_format:
        * Type: str
        * 屬性: 選填 (預設 : text)
        * 說明: 插入資料的型態，目前提供 text or json format
    * rb:
        * Type: str
        * 屬性: 選填
        * 說明: Record Begin，當插入多筆資料時，用來區別每筆資料的特定欄位 or 符號
    * Usage:
        ```
        db = 'all_col_no_weight'
        record = '@title:好麻煩@content:好不想寫Usage喔@title:妹控好壞@content:gary87'
        rb = '@title:'
        gaipy.Insert(db, record, 'text', rb)
        ```
* **Update(db, rid, new_record, modify_all, record_format, getrec)**
    * 功能: 更動單筆資料特定欄位或全部取代
    * db:
        * Type: str
        * 屬性: **必填**
        * 說明: 要建立的DB名稱
    * rid:
        * Type: int
        * 屬性: **必填**
        * 說明: 要更動資料的id
    * new_record:
        * Type: str, dict
        * 屬性: **必填**
        * 說明: 要變動的欄位或資料
    * modify_all:
        * Type: bool
        * 屬性: 選填 (預設 : False)
        * 說明: 是否全部取代該筆資料
    * record_format:
        * Type: str
        * 屬性: 選填 (預設 : text)
        * 說明: 插入資料的型態，目前提供 text or json format
    * getrec:
        * Type: bool
        * 屬性: 選填 (預設 : False)
        * 說明: 回傳時是否回傳成功的整筆資料 (True) 或是只回傳成功的rid (False)
    * Usage:
        ```
        db = 'all_col_no_weight'
        new_record = '@title:啊呀不小心打錯'
        gaipy.Insert(db, 2, new_record, False)
        ```
* **Show(db)**
    * 功能: 查看資料庫的欄位有哪些
    * db:
        * Type: str
        * 屬性: **必填**
        * 說明: 要查看欄位的DB
    * Usage:
        ```
        Show(db)
        ```
* **Drop(db)**
    * 功能: 刪除資料庫
    * db:
        * Type: str
        * 屬性: **必填**
        * 說明: 欲刪除DB的名稱
    * Usage:
        ```
        Drop(db)
        ```
* **Select(db, pattern, filter_args, mode, page_cnt, page, order_by, order)**
    * 功能: 針對欄位搜尋，pattern為空時撈取全部資料
    * db:
        * Type: str
        * 屬性: **必填**
        * 說明: 欲查詢DB的名稱
    * pattern:
        * Type: dict
        * 屬性: **必填**
        * 說明: {'val': [搜尋pattern],'col': [欄位]}，若有多個pattern可依序放入list，請看範例
    * filter_args: 
        * Type: dict
        * 屬性: 選填
        * 說明: {'val': [條件],'col': [欄位]}，若有多個條件可依序放入list
    * mode:
        * Type: str, 'AndMatch', 'OrMatch', 'BestMatch'
        * 屬性: 選填
        * 說明: 多個pattern搜尋後要依照哪種邏輯產出，
    * page_cnt:
        * Type: int
        * 屬性: 選填 (預設 : 10)
        * 說明: 一頁要取幾筆資料
    * page:
        * Type: int
        * 屬性: 選填 (預設 : 1)
        * 說明: 第幾頁
    * order_by:
        * Type: str
        * 屬性: 選填
        * 說明: 排序的依據，不傳時預設 rid
    * order:
        * Type: str
        * 屬性: 選填 (預設 : desc)
        * 說明: 降序或升序 ('asc' or 'desc')
    * Usage:
        ```
        Select(DB,{'val':['標題','內容'],'col':['title','content']},filter_args = {'val:':['>10'],'col':['viewcount']})
        ```
    * Return:
        * Type: json格式，可用dict解析
        * 回傳的['data']: {'cnt': 幾筆資料, 'recs': [**rec**]}
        * **rec**: {欄位: 欄位資料, '_rid'}
        
* **Search(db, term_list, filter_args, mode, page_cnt, page, order_by, order)**
    * 功能: 全文搜尋
    * db:
        * Type: str
        * 屬性: **必填**
        * 說明: 欲查詢DB的名稱
    * term_list:
        * Type: str
        * 屬性: **必填**
        * 說明: 欲查詢的關鍵字，多個以逗號做區別 ex: 蓋世,搜尋引擎
    * filter_args: 
        * Type: dict
        * 屬性: 選填
        * 說明: {'val': [條件],'col': [欄位]}，若有多個條件可依序放入list
    * mode:
        * Type: str, 'AndMatch', 'OrMatch', 'BestMatch'
        * 屬性: 選填
        * 說明: 多個pattern搜尋後要依照哪種邏輯產出，
    * page_cnt:
        * Type: int
        * 屬性: 選填 (預設 : 10)
        * 說明: 一頁要取幾筆資料
    * page:
        * Type: int
        * 屬性: 選填 (預設 : 1)
        * 說明: 第幾頁
    * order_by:
        * Type: str
        * 屬性: 選填
        * 說明: 排序的依據，不傳時預設 rid
    * order:
        * Type: str
        * 屬性: 選填 (預設 : desc)
        * 說明: 降序或升序 ('asc' or 'desc')
    * Usage:
        ```
        db = "abc"
        keyword = "蓋世,搜尋引擎"
        gaipy.Search(db, keyword, filter_args = {'val:':['>10'],'col':['viewcount']})
        ```
* **Del(db, rid)**
    * 功能: 刪除list中的rid資料
    * db:
        * Type: str
        * 屬性: **必填**
        * 說明: 欲刪除資料DB的名稱
    * rid:
        * Type: list of int
        * 屬性: **必填**
        * 說明: rid 可透過Select查詢拿到，或是insert時紀錄。
    * Usage:
        ```
        Del(DB,[1,2,3])
        ```
