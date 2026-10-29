"""
Slalom Capabilities Management System API

A FastAPI application that enables Slalom consultants to register their
capabilities and manage consulting expertise across the organization.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Slalom Capabilities Management API",
              description="API for managing consulting capabilities and consultant expertise")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory capabilities database
capabilities = {
    "Cloud Architecture": {
        "description": "Design and implement scalable cloud solutions using AWS, Azure, and GCP",
        "practice_area": "Technology",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": ["AWS Solutions Architect", "Azure Architect Expert"],
        "industry_verticals": ["Healthcare", "Financial Services", "Retail"],
        "capacity": 40,  # hours per week available across team
        "consultants": [
            {"email": "alice.smith@slalom.com", "level": "Advanced"},
            {"email": "bob.johnson@slalom.com", "level": "Proficient"}
        ]
    },
    "Data Analytics": {
        "description": "Advanced data analysis, visualization, and machine learning solutions",
        "practice_area": "Technology", 
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": ["Tableau Desktop Specialist", "Power BI Expert", "Google Analytics"],
        "industry_verticals": ["Retail", "Healthcare", "Manufacturing"],
        "capacity": 35,
        "consultants": [
            {"email": "emma.davis@slalom.com", "level": "Expert"},
            {"email": "sophia.wilson@slalom.com", "level": "Proficient"}
        ]
    },
    "DevOps Engineering": {
        "description": "CI/CD pipeline design, infrastructure automation, and containerization",
        "practice_area": "Technology",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"], 
        "certifications": ["Docker Certified Associate", "Kubernetes Admin", "Jenkins Certified"],
        "industry_verticals": ["Technology", "Financial Services"],
        "capacity": 30,
        "consultants": [
            {"email": "john.brown@slalom.com", "level": "Advanced"},
            {"email": "olivia.taylor@slalom.com", "level": "Emerging"}
        ]
    },
    "Digital Strategy": {
        "description": "Digital transformation planning and strategic technology roadmaps",
        "practice_area": "Strategy",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": ["Digital Transformation Certificate", "Agile Certified Practitioner"],
        "industry_verticals": ["Healthcare", "Financial Services", "Government"],
        "capacity": 25,
        "consultants": [
            {"email": "liam.anderson@slalom.com", "level": "Expert"},
            {"email": "noah.martinez@slalom.com", "level": "Proficient"}
        ]
    },
    "Change Management": {
        "description": "Organizational change leadership and adoption strategies",
        "practice_area": "Operations",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": ["Prosci Certified", "Lean Six Sigma Black Belt"],
        "industry_verticals": ["Healthcare", "Manufacturing", "Government"],
        "capacity": 20,
        "consultants": [
            {"email": "ava.garcia@slalom.com", "level": "Advanced"},
            {"email": "mia.rodriguez@slalom.com", "level": "Proficient"}
        ]
    },
    "UX/UI Design": {
        "description": "User experience design and digital product innovation",
        "practice_area": "Technology",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": ["Adobe Certified Expert", "Google UX Design Certificate"],
        "industry_verticals": ["Retail", "Healthcare", "Technology"],
        "capacity": 30,
        "consultants": [
            {"email": "amelia.lee@slalom.com", "level": "Expert"},
            {"email": "harper.white@slalom.com", "level": "Emerging"}
        ]
    },
    "Cybersecurity": {
        "description": "Information security strategy, risk assessment, and compliance",
        "practice_area": "Technology",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": ["CISSP", "CISM", "CompTIA Security+"],
        "industry_verticals": ["Financial Services", "Healthcare", "Government"],
        "capacity": 25,
        "consultants": [
            {"email": "ella.clark@slalom.com", "level": "Advanced"},
            {"email": "scarlett.lewis@slalom.com", "level": "Proficient"}
        ]
    },
    "Business Intelligence": {
        "description": "Enterprise reporting, data warehousing, and business analytics",
        "practice_area": "Technology",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": ["Microsoft BI Certification", "Qlik Sense Certified"],
        "industry_verticals": ["Retail", "Manufacturing", "Financial Services"],
        "capacity": 35,
        "consultants": [
            {"email": "james.walker@slalom.com", "level": "Proficient"},
            {"email": "benjamin.hall@slalom.com", "level": "Advanced"}
        ]
    },
    "Agile Coaching": {
        "description": "Agile transformation and team coaching for scaled delivery",
        "practice_area": "Operations",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": ["Certified Scrum Master", "SAFe Agilist", "ICAgile Certified"],
        "industry_verticals": ["Technology", "Financial Services", "Healthcare"],
        "capacity": 20,
        "consultants": [
            {"email": "charlotte.young@slalom.com", "level": "Expert"},
            {"email": "henry.king@slalom.com", "level": "Proficient"}
        ]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/capabilities")
def get_capabilities():
    return capabilities


def _find_consultant(capability: dict, email: str):
    """Return the consultant dict with the given email, or None if not found"""
    for consultant in capability["consultants"]:
        if consultant["email"] == email:
            return consultant
    return None


@app.post("/capabilities/{capability_name}/register")
def register_for_capability(capability_name: str, email: str, level: str = None):
    """Register a consultant for a capability"""
    # Validate capability exists
    if capability_name not in capabilities:
        raise HTTPException(status_code=404, detail="Capability not found")

    # Get the specific capability
    capability = capabilities[capability_name]

    # Validate consultant is not already registered
    if _find_consultant(capability, email) is not None:
        raise HTTPException(
            status_code=400,
            detail="Consultant is already registered for this capability"
        )

    # Default to the lowest skill level if not provided
    skill_levels = capability["skill_levels"]
    if level is None:
        level = skill_levels[0]
    elif level not in skill_levels:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid level. Must be one of: {', '.join(skill_levels)}"
        )

    # Add consultant
    capability["consultants"].append({"email": email, "level": level})
    return {"message": f"Registered {email} for {capability_name} at level {level}"}


@app.delete("/capabilities/{capability_name}/unregister")
def unregister_from_capability(capability_name: str, email: str):
    """Unregister a consultant from a capability"""
    # Validate capability exists
    if capability_name not in capabilities:
        raise HTTPException(status_code=404, detail="Capability not found")

    # Get the specific capability
    capability = capabilities[capability_name]

    # Validate consultant is registered
    consultant = _find_consultant(capability, email)
    if consultant is None:
        raise HTTPException(
            status_code=400,
            detail="Consultant is not registered for this capability"
        )

    # Remove consultant
    capability["consultants"].remove(consultant)
    return {"message": f"Unregistered {email} from {capability_name}"}


@app.put("/capabilities/{capability_name}/consultants/{email}/level")
def update_consultant_level(capability_name: str, email: str, level: str):
    """Update a consultant's skill level for a capability"""
    # Validate capability exists
    if capability_name not in capabilities:
        raise HTTPException(status_code=404, detail="Capability not found")

    # Get the specific capability
    capability = capabilities[capability_name]

    # Validate level is one of the capability's defined skill levels
    if level not in capability["skill_levels"]:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid level. Must be one of: {', '.join(capability['skill_levels'])}"
        )

    # Validate consultant is registered
    consultant = _find_consultant(capability, email)
    if consultant is None:
        raise HTTPException(
            status_code=400,
            detail="Consultant is not registered for this capability"
        )

    # Update level
    consultant["level"] = level
    return {"message": f"Updated {email}'s level to {level} for {capability_name}"}
