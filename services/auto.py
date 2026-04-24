import grpc
from generated import auto_pb2
from generated import auto_pb2_grpc

from db.queries.calculate_avg import get_ads_with_avg_price


class AutoAvgServicer(auto_pb2_grpc.AutoAvgCostServiceServicer):
    def AutoAvgCost(self, request, context):
        result = get_ads_with_avg_price(
            brand=request.brand or None,
            model=request.model or None,
            condition=request.condition or None,
            manufacture_year=request.manufacture_date or None,
            mileage=request.distance_covered or None,
            color=request.color or None,
            complication=request.complication or None,
        )

        ads = []
        for ad in result["listings"]:
            images = [
                auto_pb2.AdImageListResponse(image=img)
                for img in ad["images"]
            ]
            ads.append(auto_pb2.AdListResponse(
                id=ad["id"],
                images=images,
                title=ad["title"],
                price=ad["price"],
                model=ad["model_name"],
            ))

        return auto_pb2.AutoAvgCostResponse(
            avg_cost=result["avg_price"],
            ads=ads,
        )
