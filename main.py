import grpc
from concurrent import futures
from generated import auto_pb2_grpc
from service import AutoAvgServicer

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    auto_pb2_grpc.add_AutoAvgCostServiceServicer_to_server(AutoAvgServicer(), server)

    server.add_insecure_port("[::]:50051")

    print("auto_avg_service started on port 50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
