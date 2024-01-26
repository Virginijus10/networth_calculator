from PIL import Image
import PySimpleGUI as sg
import io


image = Image.open('bankas.png')
with io.BytesIO() as bio:
    image.save('bankas.png', format="PNG")
    image_data = bio.getvalue()

def calculate_net_worth(assets):
    total_net_worth = sum(asset['price'] * asset['quantity'] for asset in assets)
    individual_values = [(asset['price'] * asset['quantity']) for asset in assets]
    return total_net_worth, individual_values

def calculate_passive_income(assets):
    monthly_income = 0
    for asset in assets:
        monthly_return = asset['price'] * asset['quantity'] * (asset['yearly_return'] / 100) / 12
        monthly_income += monthly_return
    return monthly_income

sg.theme('darkblue') 

layout = [ 
    [sg.Image(size=(550, 150), filename= 'bankas.png', key= 'background')],  
    [sg.Text("Formation of an investment portfolio", size=(30, 1), font=("Helvetica", 25), text_color='blue')],
    [sg.Text("Add your assets and details below")],
    [sg.Text("Asset Name"), sg.InputText(key='asset_name', justification="right", size=(15, 10))],
    [sg.Text("Price"), sg.InputText(key='price', justification="right", size=(21, 10))],
    [sg.Text("Quantity"), sg.InputText(key='quantity', justification="right", size=(18, 10))],
    [sg.Text("Yearly Return (%) "), sg.InputText(key='yearly_return', justification="right", size=(10, 10))],
    [sg.Button("Add Asset"), sg.Button("Remove Asset"), sg.Button("Clear List")],
    [sg.Listbox(values=[], size=(55, 6), key='asset_list')],
    [sg.Text("Total Net Worth:"), sg.Text('0', size=(20, 1), key='total_net_worth')],
    [sg.Text("Budget:"), sg.InputText('10000', key='budget', justification="center", size=(17, 10))],
    [sg.ProgressBar(max_value=100, orientation='h', size=(22, 20), key='progress_bar')],
    [sg.Text("Estimated Passive Income Next Month:"), sg.Text('$0', size=(13, 1), key='passive_income')],
    [sg.Exit()]
]

window = sg.Window("Raudona skaiciuokle", layout, resizable=True)

assets = []

while True:
    event, values = window.read()

    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == "Add Asset":
        try:
            budget = float(values['budget']) 
            if not values['asset_name'] or not values['price'] or not values['quantity'] or not values['yearly_return']:
                raise ValueError("Please fill in all fields.")
            total_net_worth, _ = calculate_net_worth(assets)
            if total_net_worth + float(values['price']) * float(values['quantity']) > budget:
                raise ValueError("Adding this asset would exceed the budget.")
        
            asset_details = {
                'name': values['asset_name'],
                'price': float(values['price']),
                'quantity': float(values['quantity']),
                'yearly_return': float(values['yearly_return'])
            }
            assets.append(asset_details)
        except ValueError as e:
            sg.popup_error(str(e))

    if event == "Remove Asset":
        if values['asset_list']: 
            selected_asset_str = values['asset_list'][0]
            selected_name = selected_asset_str.split()[0]
            index_to_remove = next((i for i, asset in enumerate(assets) if asset['name'] == selected_name), None)
        if index_to_remove is not None:       
            del assets[index_to_remove]

    if event == "Clear List":
        assets.clear()

    visible_properties = ['name', 'price', 'quantity'] 
    window['asset_list'].update(values=[f"{a['name']:<20}{a['price']:<15} * {a['quantity']:^15} = ${a['price'] * a['quantity']:.2f}" for a in assets])
    
    passive_income = calculate_passive_income(assets)
    window['passive_income'].update(f"${passive_income:.2f}")

    total_net_worth, _ = calculate_net_worth(assets)
    formatted_total_net_worth = f"${total_net_worth:.2f}"
    window['total_net_worth'].update(formatted_total_net_worth)
    
    try:
        budget = float(values['budget']) 
    except ValueError:
        sg.popup_error("Please enter a valid number for net worth target.")
        continue 

    updated_net_worth, individual_values = calculate_net_worth(assets)

    if updated_net_worth < budget:
        progress = updated_net_worth / budget * 100
        window['progress_bar'].update(current_count=progress, max=100)
        None
    else:
        sg.popup_error("You do not have so much money")
window.close()    