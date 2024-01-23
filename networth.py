import PySimpleGUI as sg

def create_layout(asset_list):
    layout = [
        [sg.Text('Net Worth Tracker')],
        [sg.Listbox(values=[f'{asset}: ${price:.2f}' for asset, price in asset_list.items()],
                    size=(60, 6), key='asset_list')],
        [sg.InputText(key='new_asset', size=(20, 1)), sg.InputText(key='asset_price', size=(10, 1)),
         sg.Button('Add Asset')],
        [sg.InputText(key='new_target', size=(20, 1)), sg.Button('Add Target')],
        [sg.Text('Total Net Worth: $', size=(15, 1)), sg.Text('', size=(15, 1), key='net_worth')],
        [sg.Text("Networth Target: $", size=(15, 1)), sg.Text("", size=(15, 1), key="net_worth_target")],
        [sg.ProgressBar(max_value=100, orientation='horizontal', size=(40, 10), style='xpnative', key='progress_bar')],
        [sg.Button('Calculate progress'), sg.Button('Exit', button_color=('white', 'red'))]
    ]
    return layout

def update_net_worth(window, asset_list):
    net_worth = sum(asset_list.values())
    window['net_worth'].update(f'{net_worth:.2f}')

def update_net_worth_target(window, new_target:float):
    window['net_worth_target'].update(f'{new_target:.2f}')

def calculate_progress(window, asset_list):
    net_worth = sum(asset_list.values())
    net_worth_target_str = window['net_worth_target'].get()

    # Check if the string is not empty and contains a valid integer value
    if net_worth_target_str and net_worth_target_str.isdigit():
        net_worth_target = int(net_worth_target_str)
        progress = (net_worth / net_worth_target) * 100
        return progress
    else:
        sg.popup_error('Please enter a valid target.')
        return None  # Return an indicator that the progress couldn't be calculated


def main():
    sg.theme('LightGrey1')
    asset_list = {}

    layout = create_layout(asset_list)
    window = sg.Window('Net Worth Tracker', layout, resizable=True)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        elif event == 'Add Asset':
            new_asset_name = values['new_asset']
            new_asset_price = values['asset_price']
            if new_asset_name and new_asset_price and new_asset_price.isdigit():
                asset_list[new_asset_name] = float(new_asset_price)
                window['asset_list'].update(values=[f'{asset}: ${price:.2f}' for asset, price in asset_list.items()])
                window['new_asset'].update('')
                window['asset_price'].update('')
                update_net_worth(window, asset_list)
            else:
                sg.popup_error('Please enter a valid asset name and price.')
        elif event == "Add Target":
            new_target_input = window['new_target']
            new_target_value = new_target_input.get()  # Extract numeric value
            if new_target_value and new_target_value.isdigit():
                update_net_worth_target(window, float(new_target_value))
                window['new_target'].update('')
            else:
                sg.popup_error('Please enter a valid target value.')
        elif event == 'Calculate progress':
            new_target_input = window['new_target'].get()
            if new_target_input:
                progress_bar = window['progress_bar']
                progress_bar.update(calculate_progress(window, asset_list))
            else:
                sg.popup_error('Please enter a target.')

    window.close()

if __name__ == '__main__':
    main()
