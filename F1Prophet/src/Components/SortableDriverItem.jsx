import React from 'react';
import {useSortable} from '@dnd-kit/sortable';
import {CSS} from '@dnd-kit/utilities';
import './SortableDriverItem.css';

function SortableDriverItem({ driver, position, onRemove, isDnf }) {
    const {
        attributes,
        listeners,
        setNodeRef,
        transform,
        transition,
    } = useSortable({ id: driver.driver_id });

    const style = {
        transform: CSS.Transform.toString(transform),
        transition,
    };

    const driverImage = `/images/drivers/${driver.code}.png`;

    return (
        <div
            ref={!isDnf ? setNodeRef : null}
            style={!isDnf ? style : {}}
            className={`sortable-driver-item ${isDnf ? 'dnf-item' : ''}`}
        >
            <div className='drag-handle' {...(!isDnf ? attributes : {})} {...(!isDnf ? listeners : {})}>
                <span className='position-number'>{position === 'DNF' ? 'DNF' : `P${position}`}</span>
            </div>

            <div className='predict-driver-info'>
                <img
                    src={driverImage}
                    alt={driver.full_name}
                    className='driver-image-small'
                    onError={(e) => {
                        e.target.style.display = 'none';
                    }}
                />
                <span className='driver-code'>{driver.code}</span>
                <span className='driver-name'>{driver.full_name}</span>
            </div>

            <button
                className='remove-btn'
                onClick={() => onRemove(driver.driver_id)}
                title={isDnf ? 'Move back to finishing' : 'Mark as DNF'}
            >
                {isDnf ? <>&#8593;</> : '×'}
            </button>
        </div>
    );
}

export default SortableDriverItem;