from typing import Dict, List, Any
from mypy_boto3_s3.service_resource import Bucket

from src.clients import s3_client
from src.services.config_service import ConfigService
from src.model.dto.aws_credentials_dto import AWSCredentialsDTO

# Constants for cost estimation
COST_PER_GB_MONTH = 0.023

class ReportService:
    @staticmethod
    def get_storage_report(group_by_tags: List[str] = None) -> Dict[str, Any]:
        """
        Generates a storage report by aggregating object sizes based on S3 tags.
        
        Args:
            group_by_tags (List[str]): List of tag keys to group by. 
                                      Defaults to ["Project"].
        
        Returns:
            Dict[str, Any]: Aggregated data and totals.
        """
        if not group_by_tags:
            group_by_tags = ["Project"]
            
        bucket_resource: Bucket = s3_client.create_s3_resource()
        aws_credentials: AWSCredentialsDTO = ConfigService.get_aws_credentials()
        bucket_name = aws_credentials.bucket_name
        
        report_data = {}
        total_size_bytes = 0
        total_objects = 0
        
        # Iterate over all objects in the bucket
        for obj_summary in bucket_resource.objects.all():
            if not (obj_summary.key.endswith(".zip") or obj_summary.key.endswith(".enc")):
                continue
                
            total_objects += 1
            size = obj_summary.size
            total_size_bytes += size
            
            # Fetch tags for each object
            try:
                tags_response = bucket_resource.meta.client.get_object_tagging(
                    Bucket=bucket_name, 
                    Key=obj_summary.key
                )
                tags = {t['Key']: t['Value'] for t in tags_response.get('TagSet', [])}
            except Exception:
                tags = {}
            
            # Build grouping key
            grouping_values = []
            for tag_key in group_by_tags:
                val = tags.get(tag_key)
                
                if not val:
                    val = "Legacy/No-Tag"
                    
                grouping_values.append(val)
            
            group_key = " | ".join(grouping_values)
            
            if group_key not in report_data:
                report_data[group_key] = {
                    "size_bytes": 0,
                    "object_count": 0
                }
            
            report_data[group_key]["size_bytes"] += size
            report_data[group_key]["object_count"] += 1
            
        # Calculate costs and format
        total_gb = total_size_bytes / (1024**3)
        total_cost_est = total_gb * COST_PER_GB_MONTH
        
        final_report = {
            "groups": report_data,
            "totals": {
                "total_size_bytes": total_size_bytes,
                "total_objects": total_objects,
                "total_cost_est": total_cost_est
            }
        }
        
        return final_report
