import {bundle as archive} from './archive-bundle-v1.mjs';
const freeze=x=>{if(x&&typeof x==='object'){Object.values(x).forEach(freeze);Object.freeze(x)}return x};
export const registry=freeze([{digest:'3edbbaa0c4fa9e2fc54570ef251103c5e6bb98b93e0341872225ade5495447e7',scorer:'fixture-score-v1',bundle:archive}]);
