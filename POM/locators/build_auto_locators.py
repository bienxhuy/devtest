class BuildAppAuto:
    # Header
    HOME_HEADER = "a[//text() = 'home']"
    COURSES_HEADER = "a[//text() = 'courses']"
    RESOURCES_HEADER = "a[//text() = 'resources']"
    COMMUNITY_HEADER = "a[//text() = 'community']"
    ABOUT_HEADER = "a[//text() = 'about']"
    CONTACT_HEADER = "a[//text() = 'contact']"

    # Hero
    START_LEARNING_BUTTON = "//button[@id = 'start-learning-button']"
    WATCH_DEMO_BUTTON = "//button[@id = 'watch-demo-button']"

    # Courses
    ENROLL_COURSE_BUTTON1 = "//button[@id = 'enroll-button-1']" 
    ENROLL_COURSE_BUTTON2 = "//button[@id = 'enroll-button-2']" 
    ENROLL_COURSE_BUTTON3 = "//button[@id = 'enroll-button-3']" 
    ENROLL_COURSE_BUTTON4 = "//button[@id = 'enroll-button-4']" 
    ENROLL_COURSE_BUTTON5 = "//button[@id = 'enroll-button-5']" 
    ENROLL_COURSE_BUTTON6 = "//button[@id = 'enroll-button-6']" 

    # Resourses
    RESOURCES_BLOCK_PDF = "//div[contains(text(), 'PDF') and contains(@class, 'bg-white')]"
    RESOURCES_BLOCK_VIDEO = "//div[contains(@class, 'bg-white') and contains(., 'Video')]"
    RESOURCES_BLOCK_CODEEX = "//div[contains(@class, 'bg-white') and contains(., 'GitHub')]"
    RESOURCES_DOWNLOAD_ICON = "//svg[contains(@class, 'lucide-download')]"


    