import grpc

from generated import auto_pb2
from generated import auto_pb2_grpc


class AutoAvgServicer(auto_pb2_grpc.AutoAvgCostServiceServicer):
    def AutoAvgCost(self, request, context):
        brand = request.brand
        condition = request.condition
        model = request.model
        complication = request.complication
        manufacture_date = request.manufacture_date
        distance_covered = request.distance_covered
        color = request.color

        ads_data = []

        ads = []
        for ad in ads_data:
            images = [
                auto_pb2.AdImageListResponse(image=img)
                for img in ad["images"]
            ]
            ads.append(auto_pb2.AdListResponse(
                id=ad["id"],
                images=images,
                title=ad["title"],
                price=ad["price"],
                model=ad["model"],
            ))
        avg_cost = 15000.0
        
        return auto_pb2.AutoAvgCostResponse(
            avg_cost=avg_cost,
            ads=ads,
        )
