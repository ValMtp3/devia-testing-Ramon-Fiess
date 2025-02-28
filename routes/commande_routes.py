from flask import Blueprint, request, jsonify
from models.database import db
from models.commande import Commande

commande_routes = Blueprint("commande_route", __name__)

@commande_routes.route("/commandes", methods=["GET"])
def get_commandes():
    commandes = Commande.query.all()
    return jsonify([commande.to_dict() for commande in commandes]), 200

@commande_routes.route("/commandes/<int:commande_id>", methods=["GET"])
def get_commande(commande_id):
    commande = db.session.get(Commande, commande_id)
    if commande:
        return jsonify(commande.to_dict()), 200
    return jsonify({"error": "Commande not found"}), 404

@commande_routes.route("/commandes", methods=["POST"])
def create_commande():
    data = request.get_json()
    if not data.get("name") or not data.get("description") or not data.get("prix"):
        return jsonify({"error": "Missing required fields"}), 400

    if not isinstance(data["prix"], int):
        return jsonify({"error": "Invalid price format"}), 400

    if Commande.query.filter_by(name=data["name"]).first():
        return jsonify({"error": "Commande name already exists"}), 409

    new_commande = Commande(name=data["name"], description=data["description"], prix=data["prix"])
    db.session.add(new_commande)
    db.session.commit()
    return jsonify(new_commande.to_dict()), 201

@commande_routes.route("/commandes/<int:commande_id>", methods=["PUT"])
def update_commande(commande_id):
    commande = db.session.get(Commande, commande_id)
    if not commande:
        return jsonify({"error": "Commande not found"}), 404

    data = request.get_json()
    commande.name = data.get("name", commande.name)
    commande.description = data.get("description", commande.description)

    if "prix" in data and not isinstance(data["prix"], int):
        return jsonify({"error": "Invalid price format"}), 400
    commande.prix = data.get("prix", commande.prix)

    db.session.commit()
    return jsonify(commande.to_dict()), 200

@commande_routes.route("/commandes/<int:commande_id>", methods=["DELETE"])
def delete_commande(commande_id):
    commande = db.session.get(Commande, commande_id)
    if not commande:
        return jsonify({"error": "Commande not found"}), 404

    db.session.delete(commande)
    db.session.commit()
    return jsonify({"message": "Commande deleted successfully"}), 200