var autocomplete;
function initAutocomplete() {
    var input = document.getElementById('id_address');
    autocomplete = new google.maps.places.Autocomplete(input,
        {
            types: ['geocode', 'establishment'],
            componentRestrictions: { country: 'us' },
            // fields: ['address_components', 'geometry'],
        }
    );
    autocomplete.addListener( 'place_changed', onPlaceChanged);
    console.log('this autocomplete',autocomplete)
}

function onPlaceChanged() { 
    console.log('this autocomplete inplace',autocomplete)
        var place = autocomplete.getPlace();

        if (!place.geometry){
            document.getElementById('id_address').placeholder ="start typing..";}
        else {
            console.log('[lace name =>, ', place.name);
        }
        console.log(place) 
        let lat =place.geometry.location.lat() 
        let lng =place.geometry.location.lng() 
        let address = place.formatted_address
        
            
        for (let i of place.address_components){
            for (let j of i.types){
                if (j == "country"){
                   $('#id_country').val( i.short_name)
            }
                if (j == "administrative_area_level_1"){
                   $('#id_state').val( i.short_name)
            }
                if (j == "administrative_area_level_2"){
                   $('#id_city').val( i.short_name)
            }
                if (j == "postal_code"){
                   $('#id_pin_code').val( i.short_name)
                }
            
        }}
        
        $("#id_latitude").val(lat);
        $("#id_longitude").val(lng);
    
        }



// window.addEventListener('load', initialize);
