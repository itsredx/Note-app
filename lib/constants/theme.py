from pythra.theme import ThemeData


class AppThemes:
    light = ThemeData.light()
    # We can customize the light theme further if needed
    
    dark = ThemeData.dark()
    # Customize dark theme to match AppColors (manually copying values to avoid circular import)
    dark.background = "#2c2c2c" # AppColors.appBackgroundColorDarkMode
    dark.surface = "#2c2c2c" # AppColors.appBackgroundColorDarkMode
    dark.onBackground = "#d3d3d3" # AppColors.iconDarkMode
    dark.onSurface = "#d3d3d3" # AppColors.iconDarkMode
    
    # Map button colors to theme properties or verify usage
    # For now, we will rely on Colors.adaptive for custom widget colors

# Prepare the initial theme
initial_theme = AppThemes.dark # Default to dark as per original code preference
