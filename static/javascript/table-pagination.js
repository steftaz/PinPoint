//Creates a separate table page for every 10 rows

$('.pagination').html('')
        let rowNum = 0;
        const maxRows = 10;
        let totalRows = $('#table'+' tbody tr').length
        $("#table"+' tr:gt(0)').each(function () {
            rowNum++
            if (rowNum > maxRows) {
                $(this).hide()
            } else {
                $(this).show()
            }
        })
        if(totalRows > maxRows) {
            let pageNum = Math.ceil(totalRows/maxRows)
            for (let i = 1; i <= pageNum;) {
                $('.pagination').append('<li class="page-item" data-page="'+i+'">\<span class="page-link">'+ i++ +'<span class="sr-only">(current)</span></span>\</li>').show()
            }
        }
        $('.pagination li:first-child').addClass('active')
        $('.pagination li').on('click', function () {
            let pageNum = $(this).attr('data-page')
            let rowIndex = 0;
            $('.pagination li').removeClass('active')
            $('#table'+' tr:gt(0)').each(function () {
                rowIndex++
                if(rowIndex > (maxRows*pageNum) || rowIndex <= ((maxRows*pageNum)-maxRows)) {
                    $(this).hide()
                } else {
                    $(this).show()
                }
            })
        })