#!/usr/bin/env python3
"""
COMPREHENSIVE KPI GPT DATABASE TEST
Testing EVERY aspect of the database with various question formats
"""

from kpi_gpt_rag import create_kpi_rag_system
import time
import logging

logging.basicConfig(level=logging.WARNING)  # Reduce log noise

def test_kpi_gpt_comprehensive():
    print("🚀 COMPREHENSIVE KPI GPT DATABASE TEST")
    print("=" * 80)
    print("Testing EVERY aspect of your database with various question formats...")
    
    # Initialize system
    rag_system = create_kpi_rag_system()
    rag_system.setup_system()
    
    # COMPREHENSIVE TEST QUESTIONS - COVERING ALL DATA
    test_categories = {
        
        # 1. INSTITUTE INFORMATION
        "🏛️ Institute Information": [
            "What is Khulna Polytechnic Institute?",
            "When was KPI established?",
            "Tell me about the history of Khulna Polytechnic Institute",
            "How many students study at KPI?",
            "What is the total area of KPI campus?",
            "Is KPI under which government ministry?",
            "How far is KPI from Khulna Railway Station?",
            "What is the vision of KPI?",
            "About Digital Bangladesh and KPI's role",
            "How many permanent positions are there at KPI?"
        ],
        
        # 2. DEPARTMENTS
        "🏢 Departments & Technologies": [
            "What departments are available at KPI?",
            "List all 9 technologies at KPI",
            "Tell me about Civil Technology department",
            "What is IPCT technology?",
            "Explain RAC technology",
            "What is ENVT department?",
            "Computer Science and Technology department details",
            "All technical departments at KPI",
            "Non-technical subjects at KPI",
            "Which departments offer diploma engineering?"
        ],
        
        # 3. PRINCIPAL
        "👨‍💼 Principal Information": [
            "Who is the principal of KPI?",
            "Sheikh Mustafizur Rahman details",
            "Principal's contact information",
            "What is the principal's phone number?",
            "Email of KPI principal",
            "When did Sheikh Mustafizur Rahman become principal?",
            "How to contact the principal?",
            "Principal's office phone number",
            "Principal's mobile number",
            "Tell me about the current principal"
        ],
        
        # 4. DEPARTMENT HEADS
        "👥 Department Heads": [
            "Who is the head of Civil department?",
            "S.M. Kamruzzaman contact details",
            "Head of Computer department?",
            "Susmita Kundu information",
            "Who heads the Electrical department?",
            "Sheikh Md. Mahfuzur Rahman details",
            "Mechanical department head?",
            "Subrata Saha contact info",
            "Electronics department head?",
            "Dr. Engr. Alok Sarkar information"
        ],
        
        # 5. OFFICIALS & CHIEF INSTRUCTORS
        "🎓 Officials & Chief Instructors": [
            "List all chief instructors at KPI",
            "Who is Engr. Mobashwira Sultana Monira?",
            "Md. Shahin contact information",
            "A.K.M. Mazharul Alam details",
            "Tell me about Bimal Chandra Dewri",
            "Mina Md. Bulbul Jahan information",
            "Who is Md. Abu Darda Mali?",
            "All officials in the institute",
            "Contact all chief instructors",
            "IPCT chief instructor details"
        ],
        
        # 6. CIVIL DEPARTMENT TEACHERS
        "🏗️ Civil Department Faculty": [
            "All teachers in Civil department",
            "Tuhin Malakar contact details",
            "Who is Sabuj Chandra Roy?",
            "Md. Shakib Uddin information",
            "Kamrul Hasan details",
            "Jewel Rana contact info",
            "Civil department instructors list",
            "Md. Abbas Ali phone number",
            "Firoz Khan email address",
            "Md. Sohel Rana information"
        ],
        
        # 7. ELECTRICAL DEPARTMENT TEACHERS
        "⚡ Electrical Department Faculty": [
            "All Electrical department teachers",
            "Inzamamul Islam details",
            "Md. Waliur Rahman contact",
            "Who teaches in Electrical department?",
            "Md. Mehedi Hasan information",
            "Md. Bulbul Ahmed details",
            "Electrical instructors contact list",
            "Md. Osman Sheikh phone",
            "Md. Ashikuzzaman email"
        ],
        
        # 8. MECHANICAL DEPARTMENT TEACHERS
        "⚙️ Mechanical Department Faculty": [
            "Mechanical department teachers list",
            "Md. Israfil Alam contact",
            "A.K.M. Shahid Hasan details",
            "Debashish Chandra Dey info",
            "Md. Ruhul Amin Rana contact",
            "Md. Sabbir Ahmed details",
            "Who is Onik Roy?",
            "Tonmoy Sana information",
            "Milan contact details",
            "Avijit Mridha phone number"
        ],
        
        # 9. POWER DEPARTMENT TEACHERS
        "🔋 Power Department Faculty": [
            "Power department teachers",
            "Md. Moshiar Rahman details",
            "Md. Ahsan Habib contact",
            "Amitava Halder information",
            "Md. Suman Mia details",
            "All Power technology instructors",
            "Who teaches Power engineering?",
            "Power department faculty list"
        ],
        
        # 10. ELECTRONICS DEPARTMENT TEACHERS
        "📱 Electronics Department Faculty": [
            "Electronics department teachers",
            "Akunji Mehedi Hasan details",
            "Md. Babul contact information",
            "Md. Rajib Hossain details",
            "Nazia Nahar Shanta info",
            "Md. Shamim contact details",
            "Monishongkor Biswas information",
            "Sattyajit Sarker details",
            "Md. Shipon Hossain contact"
        ],
        
        # 11. COMPUTER DEPARTMENT TEACHERS
        "💻 Computer Department Faculty": [
            "Computer department teachers list",
            "Simanto Ghosh details",
            "Md. Sabuz Rana information",
            "Md. Mehedi Hasan contact",
            "Suchana Haldar details",
            "Arup Roy information",
            "Rinku Mallick contact",
            "Who teaches Computer Science?",
            "CST department faculty"
        ],
        
        # 12. ENVT DEPARTMENT TEACHERS
        "🌱 ENVT Department Faculty": [
            "Environmental department teachers",
            "H. M. Masud Rana details",
            "Md. Rifat Chowdhury contact",
            "Lohit Bairagi information",
            "Md. Mottakin Islam details",
            "Md. Zahidul Islam contact",
            "Md. Arifuzzaman information",
            "ENVT faculty list"
        ],
        
        # 13. IPCT DEPARTMENT TEACHERS
        "🔧 IPCT Department Faculty": [
            "IPCT department teachers",
            "Md. Saleh Nasim details",
            "Md. Ujjal Hossain contact",
            "Md. Shakil Hossain information",
            "Md. Mushfiquzzaman details",
            "Md. Mahbub Alam contact",
            "IPCT instructors list"
        ],
        
        # 14. RAC DEPARTMENT TEACHERS
        "❄️ RAC Department Faculty": [
            "RAC department teachers",
            "Emdadul Haque Khan details",
            "S. M. Salah Uddin contact",
            "Ali Ahmad Biswas information",
            "Md. Rajib Islam details",
            "Md. Asaduzzaman Khan contact",
            "Md. Khokon Mia information",
            "RAC instructors list"
        ],
        
        # 15. NON-TECH TEACHERS (INCLUDING JULEKHA)
        "📚 Non-Tech Department Faculty": [
            "All Non-Tech teachers",
            "Mahbub Alam chief instructor",
            "Mithun Sarker details",
            "Shariful Islam contact",
            "Md. Nazmul Hossain information",
            "Dipak Kumar Mondal details",
            "Liakat Hossain contact",
            "Julekha Akter Koli information",  # KEY TEST
            "Julekha Akter Koli phone number",
            "Chemistry teacher Julekha",
            "Who teaches chemistry at KPI?",
            "Md. Mostafa Morshed details",
            "Md. Al-Emran contact",
            "Hira Parvez information",
            "Prodyut Mondal details",
            "Md. Foysal Islam contact",
            "Md. Mizanur Rahman Chowdhury info",
            "Md. Imran Kabir details",
            "Md. Jewel Rana contact",
            "Ripon Hossain information",
            "Md. Foysal Ahmed details"
        ],
        
        # 16. CLUBS & ORGANIZATIONS
        "🎪 Clubs & Organizations": [
            "What clubs are available at KPI?",
            "Tell me about BNCC at KPI",
            "Rovers and Scouts information",
            "Red Crescent Society details",
            "Rangers unit at KPI",
            "ICT Training Cell information",
            "What is CODE KPI?",
            "CODE KPI contact details",
            "All student organizations",
            "Facebook page of CODE KPI",
            "CODE KPI website",
            "Upcoming AI workshop details",
            "What activities does BNCC do?",
            "How to join Scouts at KPI?"
        ],
        
        # 17. CLASS CAPTAINS - TESTING MANY STUDENTS
        "👨‍🎓 Class Captains & Students": [
            "Who is Famim Farhaz?",  # Creator
            "Riazul Islam Rafid details",
            "Abul hasan contact information",
            "MD. Mehedi Hasan captain details",
            "Mirazul Islam Miraz information",
            "Rakibul Islam contact",
            "Md Hamim Molla details",
            "Mostafizur Rahman information",
            "Tasfiya Jahan Reshmi contact",
            "Waliur Hassan Sheshir details",
            "All 1st semester captains",
            "Civil department captains",
            "Computer department captains",
            "Mechanical department captains",
            "Power department captains",
            "7th semester class captains",
            "2nd shift captains list",
            "Who are the class captains?",
            "Student representatives at KPI"
        ],
        
        # 18. CURRICULUM & SUBJECTS
        "📖 Curriculum & Subjects": [
            "Civil 1st semester subjects",
            "Electrical 2nd semester subjects",
            "Mechanical 3rd semester subjects",
            "Computer 4th semester subjects",
            "Power 5th semester subjects",
            "Electronics 6th semester subjects",
            "What subjects are in Civil 7th semester?",
            "RAC curriculum details",
            "All Mathematics courses",
            "Physics subjects in different departments",
            "Chemistry subjects list",
            "Engineering Drawing courses",
            "Project subjects in final semester",
            "Industrial Attachment details",
            "English courses at KPI"
        ],
        
        # 19. CONTACT INFORMATION QUERIES
        "📞 Contact Information": [
            "How to contact KPI?",
            "All phone numbers at KPI",
            "Email addresses of teachers",
            "Principal's contact details",
            "Emergency contact numbers",
            "Department wise contact list",
            "Mobile numbers of officials",
            "Office phone numbers",
            "How to reach specific teachers?",
            "Contact information for admissions"
        ],
        
        # 20. CREATOR & SYSTEM INFO
        "👨‍💻 Creator & System Information": [
            "Who created KPI GPT?",
            "Famim Farhaz details",
            "Creator's contact information",
            "KPI GPT features",
            "What can KPI GPT do?",
            "How was KPI GPT built?",
            "Developer information",
            "KPI GPT version details",
            "System capabilities",
            "Creator's social media"
        ],
        
        # 21. SPECIFIC NAME SEARCHES
        "🔍 Specific Name Tests": [
            "Tell me about Sheikh Mustafizur Rahman",
            "Who is Dr. Engr. Alok Sarkar?",
            "Engr. Mobashwira Sultana Monira information",
            "Find Julekha Akter Koli",
            "Search for Famim Farhaz",
            "Information about Susmita Kundu",
            "Details of Subrata Saha",
            "Who is Bimal Chandra Dewri?",
            "Find Md. Shahin",
            "Search Inzamamul Islam"
        ],
        
        # 22. PHONE NUMBER SEARCHES
        "📱 Phone Number Queries": [
            "Phone number of principal",
            "01765696900 belongs to whom?",
            "Contact number of Julekha Akter Koli",
            "01642-880100 owner details",
            "Find phone number 01992006492",
            "Mobile number of Famim Farhaz",
            "01843728903 belongs to who?",
            "Emergency contact numbers",
            "All mobile numbers at KPI"
        ],
        
        # 23. EMAIL SEARCHES
        "📧 Email Address Queries": [
            "Principal's email address",
            "principal@kpi.edu.bd details",
            "Email of computer department head",
            "susmita.bsec11@gmail.com owner",
            "famimfarhaz@gmail.com belongs to?",
            "All email addresses at KPI",
            "Official email contacts",
            "Teacher email addresses"
        ],
        
        # 24. DEPARTMENT-WISE QUERIES
        "🏛️ Department-wise Information": [
            "Everything about Civil department",
            "Complete Electrical department info",
            "All Mechanical department details",
            "Computer department full information",
            "Power department complete details",
            "Electronics department everything",
            "RAC department full info",
            "ENVT department all details",
            "IPCT department complete information",
            "Non-Tech department everything"
        ]
    }
    
    # RUN COMPREHENSIVE TESTS
    total_questions = sum(len(questions) for questions in test_categories.values())
    current_question = 0
    successful_answers = 0
    
    print(f"\n📊 Total Questions: {total_questions}")
    print("🧪 Starting comprehensive testing...\n")
    
    for category, questions in test_categories.items():
        print(f"\n{category}")
        print("=" * 60)
        
        for i, question in enumerate(questions, 1):
            current_question += 1
            print(f"\n🔍 Question {current_question}/{total_questions}: {question}")
            
            try:
                # Ask the question
                response = rag_system.query(question, max_tokens=512, temperature=0.3)
                answer = response.get('answer', 'No response')
                
                # Check if answer contains useful information (not just "I couldn't find")
                answer_lower = answer.lower()
                is_useful = not (
                    "couldn't find" in answer_lower or 
                    "not available" in answer_lower or
                    "don't have" in answer_lower or
                    len(answer) < 50
                )
                
                if is_useful:
                    successful_answers += 1
                    print(f"✅ Answer: {answer[:200]}{'...' if len(answer) > 200 else ''}")
                else:
                    print(f"❌ Answer: {answer[:100]}{'...' if len(answer) > 100 else ''}")
                
                # Small delay to avoid rate limiting
                time.sleep(0.5)
                
            except Exception as e:
                print(f"⚠️ Error: {str(e)}")
    
    # FINAL RESULTS
    success_rate = (successful_answers / total_questions) * 100
    
    print(f"\n" + "=" * 80)
    print("🎯 COMPREHENSIVE TEST RESULTS")
    print("=" * 80)
    print(f"📊 Total Questions Asked: {total_questions}")
    print(f"✅ Successful Answers: {successful_answers}")
    print(f"❌ Failed/Incomplete Answers: {total_questions - successful_answers}")
    print(f"📈 Success Rate: {success_rate:.1f}%")
    
    if success_rate >= 90:
        print("🏆 EXCELLENT! Your KPI GPT knows almost everything!")
    elif success_rate >= 80:
        print("🎉 GREAT! Your system covers most of the database well!")
    elif success_rate >= 70:
        print("👍 GOOD! System works well but has some gaps!")
    else:
        print("⚠️ NEEDS IMPROVEMENT! Some data might not be accessible!")
    
    print("\n🎊 Comprehensive testing completed!")
    print("Your KPI GPT has been thoroughly tested on ALL database content!")

if __name__ == "__main__":
    test_kpi_gpt_comprehensive()
