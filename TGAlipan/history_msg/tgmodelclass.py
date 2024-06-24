import dataclasses
import enum

@dataclasses.dataclass
class VideoInfoModel:
    id: int             # 消息id
    name: str           # 电视剧名
    episode_name: str   # 集数名 
    subscribe_url: str    # 集数链接


# aria2 下载信息
@dataclasses.dataclass
class DownloadsInfo:
    url: str          # 下载地址      
    out_name: str     # 输出文件名
    out_dir: str = "/data" # 输出文件夹

# 模块
class TGModule(enum.Enum):
    TG_API_MSG   = "TG_API_MSG  "       # 收到消息
    TG_PARSE     = "TG_PARSE_MSG"     # 解析消息
    TG_SUBSCRIBE = "TG_SUBSCRIBE"     # 阿里云订阅
    TG_DOWNLOAD  = "TG_DOWNLOAD "      # 下载文件

# 阿里云盘信息
@dataclasses.dataclass
class AliyunVideoInfo:
    name: str       # The.Double.S01E01.2024.2160p.WEB-DL.H265.HQ.AAC.mp4
    size: int       #  size=7300931589
    drive_id: str   #  '827503972'
    file_id: str    # '665c09b36f02a43fd01f495f80dc04585f77ddc2'
    mime_type: str  # 'video/mp4' or None
    created_at: str # '2024-06-02T08:18:33.057Z'
    updated_at: str # '2024-06-02T08:18:33.057Z'
    share_id: str   # '24wo9GEyRv4'
    parent_file_id: str # '665c09b36f02a43fd01f495f80dc04585f77ddc2'
    type: str       # 'file'
