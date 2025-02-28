from flask import Blueprint, request, jsonify
from models.database import db
from models.service import Service

service_routes = Blueprint("service_route", __name__)

@service_routes.route("/services", methods=["GET"])
def get_services():
    services = Service.query.all()
    return jsonify([service.to_dict() for service in services]), 200

@service_routes.route("/services/<int:service_id>", methods=["GET"])
def get_service(service_id):
    service = db.session.get(Service, service_id)
    if service:
        return jsonify(service.to_dict()), 200
    return jsonify({"error": "Service not found"}), 404

@service_routes.route("/services", methods=["POST"])
def create_service():
    data = request.get_json()
    if not data.get("name") or not data.get("description") or not data.get("prix"):
        return jsonify({"error": "Missing required fields"}), 400

    if not isinstance(data["prix"], int):
        return jsonify({"error": "Invalid price format"}), 400

    if Service.query.filter_by(name=data["name"]).first():
        return jsonify({"error": "Service name already exists"}), 409

    new_service = Service(name=data["name"], description=data["description"], prix=data["prix"])
    db.session.add(new_service)
    db.session.commit()
    return jsonify(new_service.to_dict()), 201

@service_routes.route("/services/<int:service_id>", methods=["PUT"])
def update_service(service_id):
    service = db.session.get(Service, service_id) 
    if not service:
        return jsonify({"error": "Service not found"}), 404

    data = request.get_json()
    service.name = data.get("name", service.name)
    service.description = data.get("description", service.description)

    if "prix" in data and not isinstance(data["prix"], int):
        return jsonify({"error": "Invalid price format"}), 400
    service.prix = data.get("prix", service.prix)
    
    db.session.commit()
    return jsonify(service.to_dict()), 200

@service_routes.route("/services/<int:service_id>", methods=["DELETE"])
def delete_service(service_id):
    service = db.session.get(Service, service_id) 
    if not service:
        return jsonify({"error": "Service not found"}), 404

    db.session.delete(service)
    db.session.commit()
    return jsonify({"message": "Service deleted successfully"}), 200