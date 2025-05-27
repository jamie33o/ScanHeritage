/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.html',

        /*
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        '../../templates/**/*.html',
        '../../templates/*.html',

        /*
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        '../../**/templates/**/*.html',

        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        /* JS 1: Ignore any JavaScript in node_modules folder. */
        // '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        // '../../**/*.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        // '../../**/*.py'
    ],
  theme: {
        extend: {
            colors: {
                // n0.1
                primary: " #1e1f24", // Black
                secondary: " #7cd1db", // Custom Light Blue
                dark: " #3b2b30", // Darker Black
                light: " #e6a97a", // Light Blue Variant
                accent: " #b85a3d",
                accentLight: " #f2e2d2",
                
                // no.2
                t1_bg2: " #f1a183", // Ocean Depth Blue
                t1_button: " #ed884c", // Soft Woodland Green
                t1_button_hover: " #b85a3d", // Sunset Orange
                t1_border: " #e64f25", // Warm Sunset Coral

                t2_bg2: " #f1e0ce", // Ocean Depth Blue
                t2_button: " #ec9a86", // Soft Woodland Green
                t2_button_hover: " #b85a3d", // Sunset Orange
                t2_border: " #a2c5c9", // Warm Sunset Coral

                t3_bg2: " #67ddab", // Ocean Depth Blue
                t3_button: " #909090", // Soft Woodland Green
                t3_button_hover: " #018da5", // Sunset Orange
                t3_border: " #909090", // Warm Sunset Coral

                t4_bg2: " #f1d8db", // Ocean Depth Blue
                t4_button: " #c9dcdb", // Soft Woodland Green
                t4_button_hover: " #c0b5b9", // Sunset Orange
                t4_border: " #dbd2cc", // Warm Sunset Coral
            },
            backgroundImage: {
                'custom-gradient': "radial-gradient(circle, #e6a97a, #b85a3d, #6b4d3d, #3b2b30, #1e1f24)",
                't1_bg1': "radial-gradient(circle, #f1a183, #b85a3d, #991b27, #3b2b30, #1e1f24)",
                't2_bg1': "radial-gradient(circle, #f3c262, #b85a3d, #e36255, #3b2b30, #1e1f24)",
                't3_bg1': "radial-gradient(circle, #0b9b8a, #80daeb, #018da5, #0b9b8a, #1e1f24)",
                't4_bg1': "radial-gradient(circle, #a89c96, #9e8c92, #b8a8a2, #d68a9f, #b85a3d)"

            },
        },
        fontFamily: {
            poppins: ["Poppins", "sans-serif"],
            roboto: ["Roboto", "sans-serif"],
            montserrat: ["Montserrat", "sans-serif"],
            linksFont: ["Fjalla One", "sans-serif"]
          },
        keyframes: {
            underlineGrow: {
              "0%": { width: "0%" },
              "100%": { width: "100%" },
            },
          },
          animation: {
            "underline-grow": "underlineGrow 0.3s ease-in-out forwards",
          },
    },
    safelist: [
          // ✅ Added T1 - T4 theme classes to safelist
        "bg-t1_bg1", "bg-t1_bg2", "bg-t2_bg1", "bg-t2_bg2", "bg-t3_bg1", "bg-t3_bg2", "bg-t4_bg1", "bg-t4_bg2",
        "bg-t1_button", "hover:bg-t1_button_hover", "border-t1_border",
        "bg-t2_button", "hover:bg-t2_button_hover", "border-t2_border",
        "bg-t3_button", "hover:bg-t3_button_hover", "border-t3_border",
        "bg-t4_button", "hover:bg-t4_button_hover", "border-t4_border"
    ],
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
