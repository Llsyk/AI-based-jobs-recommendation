from PIL import ImageTk, Image, ImageFilter
import tkinter as tk
from tkinter import ttk
import subprocess
import sys
import re

def prolog_query(query):
    print("Sending Prolog Query:", query)  # Debugging line
    prolog_process = subprocess.Popen(
        ['swipl', '-q', '-f', r'C:\ai_project\company.pl', '-g', query, '-t', 'halt'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, errors = prolog_process.communicate()
    output_str = output.decode('utf-8')
    errors_str = errors.decode('utf-8')
    print("Prolog Output:", output_str)  # Debugging line
    print("Prolog Errors:", errors_str)  # Debugging line
    return output_str, errors_str

def recommend_job(skills):
    formatted_skills = ",".join([f"'{skill}'" for skill in skills])  # Convert skills to Prolog atoms
    query = f"recommend_job([{formatted_skills}], RecommendedJob, RelatedCompanies)."
    result, _ = prolog_query(query)  # Use only the output, ignore errors
    result_lines = result.strip().split('],')
    recommendations = []
    for recommendation in result_lines:
        print(recommendation)
        recommendation_info = recommendation.replace('[', '').replace(']', '').replace('Selected recommendations: ','').split('-')
        print(recommendation_info)
        recommendations.append(recommendation_info)
    return recommendations

def recommend_jobs():
    selected_skills = [skill for skill, var in skill_vars.items() if var.get()]
    if not selected_skills:
        # Clear existing job tables
        clear_job_tables()
        # Display a message
        message_label = ttk.Label(right_canvas_frame, text="Please choose at least one skill", font=("Helvetica", 12), background='#e1edfd')
        message_label.pack(padx=10, pady=5)
        return

    recommended_jobs = recommend_job(selected_skills)

    # Sort the recommended jobs by suitability percentage (descending order)
    if recommended_jobs:
        recommended_jobs.sort(key=lambda x: float(x[1]), reverse=True)
    else:
        print("No recommended jobs available.")


    # Determine the maximum height and width of the tables
    height = 100
    width = 200
    num_columns = 4  # Assuming there are four columns in each table
    for job_info in recommended_jobs:
        for item in job_info:
            
            width = max(width, len(str(item)))

    # Clear existing job tables
    clear_job_tables()

    # Add data to the job tables
    for job_info in recommended_jobs:
        job_title, suitability, company, skills_left = job_info
        skills_left = re.sub(r'\n_[0-9]*', '', skills_left)
        #skills_left = re.split(r'_[0-9]*', skills_left)
        suitability = f"{float(suitability):.2f}"

        # Insert a new job table with maximum size
        add_job_table(job_title, suitability, company, skills_left, height, width)





def clear_job_tables():
    for child in right_canvas_frame.winfo_children():
        child.destroy()

def add_job_table(job_title, suitability, company, skills_left, table_height, table_width):
    job_table_frame = ttk.Frame(right_canvas_frame, style="Custom1.TFrame", borderwidth=0, relief="solid", height=table_height, width=table_width)
    job_table_frame.pack(padx=10, pady=5)

    job_table = ttk.Frame(job_table_frame, style="Custom1.TFrame")
    job_table.pack(padx=10, pady=5)

    # Job Title
    label_title = ttk.Label(job_table, text="Job Title:", font=("Helvetica", 12, "bold"), background='white')
    label_title.grid(row=0, column=0, padx=8, pady=5, sticky="w")
    label_title_value = ttk.Label(job_table, text=job_title, font=("Helvetica", 12), background='white')
    label_title_value.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    # Suitability
    label_suitability = ttk.Label(job_table, text="Suitability:", font=("Helvetica", 12, "bold"), background='white')
    label_suitability.grid(row=1, column=0, padx=8, pady=5, sticky="w")
    label_suitability_value = ttk.Label(job_table, text=str(suitability)+" %", font=("Helvetica", 12), background='white')
    label_suitability_value.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    # Company
    label_company = ttk.Label(job_table, text="Company:", font=("Helvetica", 12, "bold"), background='white')
    label_company.grid(row=2, column=0, padx=8, pady=5, sticky="w")
    label_company_value = ttk.Label(job_table, text=company, font=("Helvetica", 12), background='white')
    label_company_value.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    # Skills Left
    label_skills_left = ttk.Label(job_table, text="Skills Left:", font=("Helvetica", 12, "bold"), background='white')
    label_skills_left.grid(row=3, column=0, padx=8, pady=5, sticky="w")
    label_skills_left_value = ttk.Label(job_table, text=skills_left, font=("Helvetica", 12), background='white', wraplength=400)
    label_skills_left_value.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    # Add a separator line
    separator = ttk.Separator(job_table_frame, orient='horizontal')
    separator.pack(fill='x', pady=5)

root = tk.Tk()
root.title("Job Recommendation System")
root.configure(background='#e1edfd')  # Set the background color of the root window

# Set window size
window_width = 1200
window_height = 500

# Calculate the position of the window to center it on the screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Configure the style for Custom.TFrame
style = ttk.Style()
style.configure("Custom.TFrame",height=100,width=200, background='#e1edfd')
style.configure("Custom1.TFrame",height=100,width=200, background='white')
style.configure("Custom2.TFrame",height=100,width=200, background='#e1edfd')
# Create a Frame for the left side (label, button, and canvas)
left_frame = ttk.Frame(root, style="Custom.TFrame")
left_frame.pack(padx=30, pady=5, side=tk.LEFT)

# Label above the checkbox frame
skills_label = ttk.Label(left_frame, text="Choose Your skills for our advice", font=("Helvetica", 18), background='#e1edfd')
skills_label.pack(pady=5)

# Create a Frame for the checkboxes
checkbox_frame = ttk.Frame(left_frame, style="Custom.TFrame")
checkbox_frame.pack(padx=10, pady=5)

# Create a Canvas to put the Frame in
canvas = tk.Canvas(checkbox_frame)
canvas.pack(side="left", fill="both", expand=True)

# Add a Scrollbar and attach it to the Canvas
scrollbar = ttk.Scrollbar(checkbox_frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")
canvas.configure(yscrollcommand=scrollbar.set)

# Create another frame to contain the checkboxes inside the Canvas
inner_frame = ttk.Frame(canvas)
canvas.create_window((0, 0), window=inner_frame, anchor="nw")

techskills = sorted(['programming', 'data_analyzing', 'web', 'java', 'python','algorithms','software_development',
                     'problem_solving','statistics','data_visualization','sql','excel',
                     'html','css','javascript','responsive_design','frontend','backend','networking',
          'routing','switching','security','trouble_shooting','tcpip','ux_design','ui_design','prototyping','user_research',
          'adobe_creativecloud','machine_learning','data_mining','deep_learning','neural_networks','tensorflow','pytorch','project_management',
          'leadership','communication','risk_management',
          'agile','cybersecurity','ethical_hacking','penetration_testing','incident_response','firewalls','database_administration',
          'database_management','normalization','indexing','mobile_development','ios','android','react_native','flutter','mobileux'])

engineerskills = sorted(['civil_engineering', 'structural_design', 'autocad', 'geotechnical_engineering','medicine', 
                         'mechanical_engineering', 'thermodynamics', 
'materials_engineering',
          'electrical_engineering', 'circuit_design', 'power_distribution','aerospace_engineering', 'aerodynamics', 
          'propulsion','environmental_engineering', 
'water_quality', 'air_pollutioncontrol', 'environmental_impact_assessment','chemical_engineering', 'process_engineering', 
'materials_chemistry', 
'safety_engineering','electronics_engineering', 
          'digital_circuits', 'analog_electronics', 'embedded_systems','industrial_engineering', 'operation_sresearch',
            'supply_chain_management', 
'quality_control'])

medicalskills = sorted([
'medicine', 'diagnostics', 'patientcare', 'surgery', 'medical_research',
'nursing',  'healthcare_administration', 'clinical_skills','pharmacy', 'medication_management', 'pharmaceutical_sciences',
 'patient_education','physical_therapy', 'rehabilitation', 'musculoskeletal_systems', 'therapeutic_exercise',
          'radiology', 'medical_imaging', 'diagnostic_interpretation', 'radiation_therapy'])

financeskills = sorted(['investment_banking', 'mergersandacquisitions', 'capital_markets','financial_planning', 'wealth_management',
                         'investment_strategies', 'risk_assessment',
           'credit_analysis', 'financial_risk_assessment', 'loan_evaluation', 'credit_reporting','auditing', 'financial_accounting',
             'internal_controls','financial_consulting', 'businessvaluation', 'investment_management'])

field = sys.argv[1]
skill_vars = {}
if field == 'technical':
    skills=techskills
elif field == 'engineer':
    skills = engineerskills
elif field == 'medical':
    skills = medicalskills
else:
    skills = financeskills

for i, skill in enumerate(skills):
    var = tk.BooleanVar()
    skill_vars[skill] = var
    # Calculate row and column for two-column layout
    row = i // 2
    column = i % 2
    checkbox = ttk.Checkbutton(inner_frame, text=skill, variable=var)
    checkbox.grid(row=row, column=column, padx=8, pady=2, sticky="w")

# Update the scroll region to include the inner_frame
inner_frame.update_idletasks()
canvas.configure(scrollregion=canvas.bbox("all"))

# Button to recommend jobs
continue_button = tk.Button(left_frame, text="Recommend Jobs", command=recommend_jobs, bg="orange", fg="white", font=("TkDefaultFont", 12, "bold"))
continue_button.pack(pady=10)

# Create a Frame for the right side (recommended jobs display)
right_frame = ttk.Frame(root,style="Custom2.TFrame")
right_frame.pack(padx=3, pady=1, side=tk.RIGHT)
recommended_jobs_frame = ttk.Frame(right_frame, style="Custom2.TFrame")
recommended_jobs_frame.pack(padx=3, pady=1, side=tk.TOP, fill=tk.BOTH, expand=True)

# Recommended jobs label above the right canvas
recommended_jobs_label = ttk.Label(recommended_jobs_frame, text="Recommended Jobs:", font=("Helvetica", 18), background='#e1edfd')
recommended_jobs_label.pack(pady=5, side=tk.LEFT)

# Create a Canvas for recommended jobs to enable scrolling
right_canvas = tk.Canvas(right_frame,height=300,width=700, background='#e1edfd')
right_canvas.pack(side="left", fill="both", expand=True)

# Add a Scrollbar and attach it to the Canvas
right_scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=right_canvas.yview)
right_scrollbar.pack(side="right", fill="y")
right_canvas.configure(yscrollcommand=right_scrollbar.set)

def back():
    root.destroy()
    subprocess.call(["python", "page2.py"])

back = tk.Button(left_frame,text='Back',bg="orange", fg="white", font=("TkDefaultFont", 12, "bold"),command=back)
back.pack(padx=10, pady=25)

# Create another frame to contain the job tables inside the Canvas
right_canvas_frame = ttk.Frame(right_canvas, style="Custom2.TFrame")
right_canvas.create_window((0, 0), window=right_canvas_frame, anchor="nw")

# Bind the frame to the scrollbar
right_canvas_frame.bind(
    "<Configure>",
    lambda e: right_canvas.configure(
        scrollregion=right_canvas.bbox("all")
    )
)

# Make the Canvas scrollable
right_canvas.bind_all("<MouseWheel>", lambda e: right_canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

# Recommended jobs display as individual tables


# Start the Tkinter event loop
root.mainloop()
