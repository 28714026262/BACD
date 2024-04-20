import math
import re
from collections import Counter

# 简单对URL进行Protocol，domain，path和query进行区分，为的是在进行cosine相似性计算时仅对query和param部分进行计算
# 前面的部分仅用来作是否进行相似性计算的判断
class URLFilter:
    def __init__(self) -> None:
        self.protocol = ""
        self.domain = ""
        self.path = ""
        self.query_param = ""

    def get_URL_Route(self, url: str) -> list:
        if url.startswith("http"):
            self.protocol = "http"
            url = url[7:]
        if url.startswith("https"):
            self.protocol = "https"
            url = url[8:]

        route_list = url.split('/')
        self.domain = route_list[0]
        self.query_param = route_list[-1]
        path_list_1 = url.split(self.domain)
        path_list_2 = path_list_1[1].split(self.query_param)
        self.path = path_list_2[0]

# 将单个URL进行向量化后进行数据存储
class URLVector:
    def __init__(self) -> None:
        self.URL = ""
        self.vector = {}
        self.filtered_url = ""
        self.filter_url = URLFilter()

    def append_url_vector(self, url):
        self.URL = url
        self.filter_url.get_URL_Route(url)
        self.filtered_url = self.filter_url.query_param
        self.text_to_vector()

    # 将URL分析成bag-of-words，这里仅对query和param部分向量化
    def text_to_vector(self):
        WORD = re.compile(r"\w+")
        words = WORD.findall(self.filtered_url)
        self.vector = Counter(words)

# 对比URL pair的相似性后，进行数据存储
class ClusterData:
    def __init__(self) -> None:
        # 存储URL pair各别的URLVector类
        self.vec_list = []
        # 存储cosine相似性
        self.cos_sim = 0
        # 存储这是第几个受处理的pair
        self.counter = 0

    def append_data(self, counter, vec_list, cos_sim):
        self.vec_list = vec_list
        self.cos_sim = cos_sim
        self.counter = counter

# WebPage聚类主类
class WebPageCluster:
    def __init__(self) -> None:
        # 将每个URL存储为URLVector类
        self.URLVector_set = []
        # 将URL pair的Cluster Data进行存储
        self.Cluster_set = []

        # 记录URL pair数目
        self.length = 1

        # 记录各个pair的cosine相似性
        self.cos_sim = []
        # 记录聚类后的WebPage情况
        self.Cluster_final = []

    # 聚类函数
    def get_cluster(self, url_list):
        for url in url_list:
            URLVector_tmp = URLVector()
            URLVector_tmp.append_url_vector(url)
            self.URLVector_set.append(URLVector_tmp)

        temp = []
        url_tmp_holder = []
        for i in self.URLVector_set:
            temp.append(i)
            for j in self.URLVector_set:
                if j == i or j in temp:
                    continue
                else:
                    # 若URL pair的domain和path不相同，则直接定义为不相似
                    if i.filter_url.domain != j.filter_url.domain or i.filter_url.path != j.filter_url.path:
                        cosine = 0.0
                        cluster_temp = ClusterData()
                        cluster_temp.append_data(self.length, [i, j], cosine)
                        self.Cluster_set.append(cluster_temp)
                        self.length += 1
                    else:
                        cosine = self.calc_cosine(i, j)
                        if cosine != 0.0:
                            # 对URL pair进行聚类
                            # 先对[url1, url2]这样的list进行存储
                            if self.Cluster_final:
                                for item in self.Cluster_final:
                                    if isinstance(item, list):
                                        if i.URL in item:
                                            if j.URL not in item:
                                                item.append(j.URL)
                                                url_tmp_holder.append(j.URL)
                                        elif j.URL in item:
                                            if i.URL not in item:
                                                item.append(i.URL)
                                                url_tmp_holder.append(i.URL)
                                        else:
                                            self.Cluster_final.append([i.URL, j.URL])
                                            url_tmp_holder.append(i.URL)
                                            url_tmp_holder.append(j.URL)
                            else:
                                self.Cluster_final.append([i.URL, j.URL])
                                url_tmp_holder.append(i.URL)
                                url_tmp_holder.append(j.URL)
                        cluster_temp = ClusterData()
                        cluster_temp.append_data(self.length, [i,j], cosine)
                        self.Cluster_set.append(cluster_temp)
                        self.length += 1

        # 再对单个URL进行存储
        for i in url_list:
            if i not in url_tmp_holder:
                self.Cluster_final.append(i)
                url_tmp_holder.append(i)
        #print(self.Cluster_final)

    # 计算cosine相似性
    def calc_cosine(self, vec1, vec2):
        intersection = set(vec1.vector.keys()) & set(vec2.vector.keys())
        numerator = sum([vec1.vector[x] * vec2.vector[x] for x in intersection])

        sum1 = sum([vec1.vector[x] ** 2 for x in list(vec1.vector.keys())])
        sum2 = sum([vec2.vector[x] ** 2 for x in list(vec2.vector.keys())])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)

        if not denominator:
            return 0.0
        else:
            return float(numerator) / denominator

URLCluster = WebPageCluster()