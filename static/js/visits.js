/** 
 * jQuery module for representation information about statistics of visits of tht website.
 * 
 * All information fetched from server by ajax.
*/
(function visitStatisticsRender() {
    //This ajax request fills select control up with pages which are under visits tracker.
    //First elelemt of select control is general statistics of visits of whole website.
    //Response is consists of urls of pages which are under visits tracker.
    $.ajax('statistic_pages', { method: 'GET', dataType: 'text',
        success: function(data){
            let stat_pages = JSON.parse(data);
            let sorted_pages = [];
            let i = 0;
            for(page in stat_pages)
                sorted_pages.push(page);
            sorted_pages.sort();
            let buf_obj = {};
            for(i in sorted_pages)
                buf_obj[sorted_pages[i]] = stat_pages[sorted_pages[i]];    
            stat_pages = buf_obj;
            $('#statistic_pages', 'main').append($('<select><option value="">Общая статистика по сайту</option></select>'));
            i = 0;
            for(let page in stat_pages){
                //To get page caption of visited url here is other ajax request which gets page name from its breadcrumbs
                $.ajax(page, {method: 'GET', dataType: 'html',
                success: function(data, status, jqXHR){
                    //We need just last item of breadcrumbs, other items replaced with text './'
                    stat_pages[page] = $('.breadcrumbs', data).text().replace(/[^\/]*\//g, './');
                },
                complete: function(){
                    i++;
                    if (i === sorted_pages.length)
                        //After all page names are received this code fills select control up
                        for(page in stat_pages){
                            if (stat_pages[page])
                                $('#statistic_pages', 'main').children('select').append($('<option value="' + page + '">' + stat_pages[page] + '</option>'));
                        }
                }});
            }    
            //Setting up event handler to catch change event of select control.
            //When user picks up item from select control next ajax request gets statistics of required page
            $('#statistic_pages', 'main').children('select').on('change', function(){
                $.ajax('json?key='+$(this).val(), {method: 'GET', dataType: 'text', 
                    success: renderStatistics,
                    error: function(jqXHR, status){
                        totalStat = undefined;
                    },
                });
            });
        }
    });
    //General statistics of visits are received by ajax at first page load
    $.ajax('json', {method: 'GET', dataType: 'text', 
        success: renderStatistics,
        error: function(jqXHR, status){
            totalStat = undefined;
        },
    });
    /** This function parses json-object of statistics of visits and build up tables and filters to present information */
    function renderStatistics(data){
        let totalStat;
        totalStat = JSON.parse(data);
        if (totalStat){ 
            let $stat_block = $('#statistics_of_visits', 'main');
            $stat_block.children('section.total').html('<span>General</span><ul></ul>');    
            $stat_block.children('section.details').html('<span>Details</span>');
            //Statistics data is contained in object which have 2 main properties: total - general stats and details - detailed stats    
            for(key in totalStat['total'])
                $('section.total ul', $stat_block).append($('<li>'+key+' : '+totalStat['total'][key]+'</li>'));
            for(key in totalStat['details']){
                //detailed stats is divided into tables which have filters in their headers
                //filters are properties of 'details' object. filters are words divided by symbol '_', i.e. country_city_year
                let filters = key.split('_');
                $stat_block.children('section.details').append($('<div class="filter '+ key +'"></div>'));   
                $('div.filter.'+key, $stat_block).append('<span>'+filters.join(', ')+'</span>');
                $('div.filter.'+key, $stat_block).append('<table class="'+key+'" border="1" cellspacing="0"></table>');
                //table of statistics have n+1 columns, where n is number of filters plus one column for visits values
                //row for the header of the table
                let $header_row = $('<tr></tr>').addClass('header');
                for(i in filters)
                    $header_row.append('<th></th>');
                $header_row.append('<th></th>');
                let $row_template = $('<tr></tr>');
                //columns for storing filters
                for(i in filters)
                    $row_template.append('<td></td>');
                //column for storing visits
                $row_template.append('<td></td>');
                //summary of the table is stored in last row with clss .footer
                let $footer_row = $('<tr></tr>').addClass('footer');
                $footer_row.append('<td colspan="' + filters.length +'"></td>');
                $footer_row.append('<td></td>');
                $('table.'+key, $stat_block).append($header_row);
                /** Function for filling up select controls of each filter after picking up filter value
                 * 
                 * Every time user picks up filter value in select control, this function rebuilds control's items.
                 * Function fills up select control by values which are visible in column of the table.
                 * This behaviar guarantees that 'select' control of the filter will store only actual values in this time
                 */
                function fillUpFilter($select, val){
                    let index = $('select', $select.closest('tr')).index($select);
                    let $tbody = $select.closest('tbody');
                    //Set-object for storing unique values of column according to vaisible rows
                    $select.data('current', new Set());
                    $select.html('<option value="all">all</option>');
                    //selector picks only visible rows of the table
                    $('tr:not(.header,.footer):visible', $tbody).children('td:nth-child(' + (index + 1) + ')').each(function(){
                        $select.data('current').add($(this).text());
                    });
                    //Select-control will be filled up by unique values of set-object
                    let sorted_arr = Array.from($select.data('current')).sort();
                    sorted_arr.forEach((s) => $select.append($('<option value="' + s.replace(/[ -]/g,'') + '">' + s +'</option>')));
                    $select.val(val);
                }
                //Cycle for creating 'select' control for each filter and putting it into column of the header.
                //There is Set-object for each select-control intended for storing unique values
                for(i in filters){
                    let $newFilter = $('<select class="'+ filters[i]+'" size="1"><option value="all">all</option></select>').clone();
                    $newFilter.attr('name', filters[i]);
                    $newFilter.data('all', new Set());
                    $($('table.'+key, $stat_block).find('tr.header').children('th')[i]).append($newFilter); 
                }
                //Last column of the header has name 'visits'
                $('table.'+key, $stat_block).find('tr.header').children('th').last().text('visits'); 
                //Filling up table and filters
                //This variable stores sum of the total visits to show it in footer of the table
                let sum = 0;
                for(val in totalStat['details'][key]){
                    let vals = val.split(':');
                    //Filling up set-object to distinguish unique values
                    for(i in filters)
                        $('select.' + filters[i], 'table.'+key).data('all').add(vals[i]); 
                    //Each tr-element of the row with data has class which contains values of each column.
                    //This class is intended to filter rows that has value picked up in the select-control of filter. 
                    //All spaces in classes are replaced by '-' symbol 
                    $('table.'+key, $stat_block).append($row_template.clone().addClass((vals.map(elem => {return elem.replace(/[ -]/g,'')})).join(' ')));
                    for(i in vals)
                        $($('table.'+key, $stat_block).find('tr').last().children('td')[i]).text(vals[i]);
                    $('table.'+key, $stat_block).find('tr').last().children('td').last().text(totalStat['details'][key][val]);
                    //Total visits
                    sum += parseInt(totalStat['details'][key][val]);
                }
                //Last row classed by footer value stores total vissits on the last column
                $('table.'+key, $stat_block).append($footer_row);
                $('table.'+key, $stat_block).find('tr.footer').children('td').first().text('total');
                $('table.'+key, $stat_block).find('tr.footer').children('td').last().text(sum);
                //After building table we can fill up select-controls of the filters
                for(i in filters){
                    //Each select-control filled up by unique values from set-object linked to it
                    let $obj = $('select.' + filters[i], 'table.'+key);
                    let sorted_arr = Array.from($obj.data('all')).sort()
                    for(s in sorted_arr)
                        $obj.append($('<option value="' + sorted_arr[s].replace(/[ -]/g,'') + '">' + sorted_arr[s] +'</option>'));
                    //Event-handler proccesses changing of the select-control.
                    //User picks up value in the filter then event-handler shows only rows of the table that contains required value
                    $obj.on('change', function(){
                        let $this = $(this);
                        let $tr = $this.closest('tr');
                        let $tbody = $this.closest('tbody');
                        let $selects = $('select', $tr);
                        let vals = [];
                        //All spaces in values of the select-control are replaced by '-' symbol 
                        $selects.each((index, elem) => vals.push($(elem).val().replace(/[ -]/g,'')));
                        //All data rows of the table are set invisible before turn-on filter
                        $tbody.children('tr').not('.header,.footer').hide();
                        //Building up query selector string based on the class list from picked up values of the all filters of the table 
                        val_ = vals.filter(p => {return (p)&&(p !== 'all')}).join('.');
                        //Setting up visible only rows which has picked up values of the filter among their class list
                        $tbody.children('tr'+ ((val_ === '') ? '' : '.' + val_)).not('.header,.footer').show();
                        //Recalculating total sum of the visits of the visible rows
                        let sum = 0;
                        $tbody.children('tr'+ ((val_ === '') ? '' : '.' + val_)).not('.header,.footer').children('td:last-child').each((index, elem) => {
                            sum += parseInt($(elem).text());
                        });
                        $tbody.children('tr.footer').children('td').last().text(sum);
                        //After showing required data rows we must rebuild value of the filters,
                        //because filter must contains only values which are located among visible rows  
                        $selects.each((index, elem) => {fillUpFilter($(elem), vals[index])});
                    });
                    //Table shows all rows by default
                    fillUpFilter($obj, 'all');
                }                       
            }
        }        
    }
})();
