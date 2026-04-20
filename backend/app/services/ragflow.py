import httpx
from typing import Optional, Dict, Any
from app.core.config import settings


class RAGFlowService:
    """RAGFlow API 服务类"""
    
    def __init__(self):
        self.base_url = settings.RAGFLOW_API_URL.rstrip('/')
        self.token = settings.RAGFLOW_API_TOKEN
        self.default_dataset_id = settings.RAGFLOW_DEFAULT_DATASET_ID
    
    def _get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers
    
    async def create_dataset(self, name: str, description: str = "") -> Optional[Dict[str, Any]]:
        """创建数据集"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/api/v1/datasets",
                    headers=self._get_headers(),
                    json={
                        "name": name,
                        "description": description
                    },
                    timeout=30.0
                )
                if response.status_code == 200:
                    return response.json().get("data")
                return None
            except Exception as e:
                print(f"创建数据集失败: {e}")
                return None
    
    async def get_datasets(self) -> list:
        """获取数据集列表"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/api/v1/datasets",
                    headers=self._get_headers(),
                    timeout=30.0
                )
                if response.status_code == 200:
                    return response.json().get("data", [])
                return []
            except Exception as e:
                print(f"获取数据集列表失败: {e}")
                return []
    
    async def upload_document(
        self, 
        dataset_id: str, 
        file_path: str, 
        file_name: str
    ) -> Optional[Dict[str, Any]]:
        """上传文档到数据集"""
        async with httpx.AsyncClient() as client:
            try:
                with open(file_path, "rb") as f:
                    files = {"file": (file_name, f)}
                    response = await client.post(
                        f"{self.base_url}/api/v1/datasets/{dataset_id}/documents",
                        headers=self._get_headers(),
                        files=files,
                        timeout=60.0
                    )
                if response.status_code == 200:
                    return response.json().get("data")
                print(f"上传文档失败: {response.text}")
                return None
            except Exception as e:
                print(f"上传文档异常: {e}")
                return None
    
    async def parse_document(self, dataset_id: str, document_id: str) -> bool:
        """解析文档"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/api/v1/datasets/{dataset_id}/documents/{document_id}/parse",
                    headers=self._get_headers(),
                    timeout=30.0
                )
                return response.status_code == 200
            except Exception as e:
                print(f"解析文档失败: {e}")
                return False
    
    async def get_document_status(self, dataset_id: str, document_id: str) -> Optional[Dict[str, Any]]:
        """获取文档解析状态"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/api/v1/datasets/{dataset_id}/documents/{document_id}",
                    headers=self._get_headers(),
                    timeout=30.0
                )
                if response.status_code == 200:
                    return response.json().get("data")
                return None
            except Exception as e:
                print(f"获取文档状态失败: {e}")
                return None
    
    async def upload_and_parse(
        self, 
        file_path: str, 
        file_name: str, 
        dataset_id: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """上传并解析文档"""
        # 使用默认数据集或指定数据集
        target_dataset_id = dataset_id or self.default_dataset_id
        
        # 如果没有指定数据集，尝试获取或创建默认数据集
        if not target_dataset_id:
            datasets = await self.get_datasets()
            if datasets:
                target_dataset_id = datasets[0].get("id")
            else:
                # 创建默认数据集
                dataset = await self.create_dataset("默认知识库", "系统默认知识库")
                if dataset:
                    target_dataset_id = dataset.get("id")
        
        if not target_dataset_id:
            print("无法获取或创建数据集")
            return None
        
        # 上传文档
        doc_result = await self.upload_document(target_dataset_id, file_path, file_name)
        if not doc_result:
            return None
        
        document_id = doc_result.get("id")
        if not document_id:
            print("上传文档成功但未获取到文档ID")
            return None
        
        # 解析文档
        parse_success = await self.parse_document(target_dataset_id, document_id)
        
        return {
            "dataset_id": target_dataset_id,
            "document_id": document_id,
            "parse_initiated": parse_success,
            "file_name": file_name
        }


# 创建全局服务实例
ragflow_service = RAGFlowService()