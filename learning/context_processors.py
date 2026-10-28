def accessibility_preferences(request):
    """Expose non-identifying display preferences stored in the Django session."""
    return {
        "high_contrast": request.session.get("high_contrast", False),
        "sound_enabled": request.session.get("sound_enabled", False),
        "narration_enabled": request.session.get("narration_enabled", False),
    }
