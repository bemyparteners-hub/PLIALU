/* ============================================================
 * PLIALU — Storage helpers (auto-save + indicateur)
 * ------------------------------------------------------------
 * Helpers partagés pour la sauvegarde automatique des modules
 * (calculette, devis, dessinateur, configurateur) et l'affichage
 * de l'indicateur visuel "💾 Projet sauvegardé".
 *
 * API
 * ----
 *   PlialuStorage.forKey(key)
 *     Pour un module qui écrit sur SA PROPRE clé localStorage
 *     (le configurateur écrit sur 'plialu-configurateur-session').
 *     Retourne { key, load, save, clear }.
 *
 *   PlialuStorage.forSubkey(rootKey, subKey)
 *     Pour un module qui partage une clé racine avec d'autres
 *     (calcul, devis, dessinateur partagent 'plialu_project_data'
 *     avec une sous-clé chacun). Pattern read-merge-write.
 *     Retourne { rootKey, subKey, load, save, clear }.
 *
 *   PlialuStorage.showIndicator(message?)
 *     Affiche le toast bas-droite "💾 Projet sauvegardé" pendant
 *     1,8s. Crée l'élément DOM à la volée si absent. Le message
 *     par défaut est "💾 Projet sauvegardé".
 *
 * Contrats
 * --------
 *   - load() retourne TOUJOURS `null` si aucune donnée n'est
 *     stockée (ou si le JSON est corrompu) ; l'objet décodé
 *     sinon. Les pages doivent tester `if (!data) { … defaults }`.
 *   - save(data) déclenche showIndicator() automatiquement.
 *   - clear() NE déclenche PAS showIndicator() (c'est un reset,
 *     pas une sauvegarde).
 *
 * Markup
 * ------
 *   Aucun. L'indicateur est créé dynamiquement avec la classe
 *   .plialu-save-indicator définie dans
 *   shared/components/save-indicator.css.
 *
 * Inclusion
 * ---------
 *   <link rel="stylesheet" href="…/shared/components/save-indicator.css">
 *   <script src="…/shared/js/storage.js"></script>
 *
 *   Le <script> peut être chargé en fin de <head> ou avant le
 *   <script> de la page qui le consomme — l'important est qu'il
 *   précède l'usage de window.PlialuStorage.
 * ============================================================ */

(function (global) {
  'use strict';

  var INDICATOR_ID = 'plialu-save-indicator';
  var INDICATOR_CLASS = 'plialu-save-indicator';
  var VISIBLE_CLASS = 'is-visible';
  var DEFAULT_MESSAGE = '💾 Projet sauvegardé';
  var FADE_MS = 1800;

  function showIndicator(message) {
    var el = document.getElementById(INDICATOR_ID);
    if (!el) {
      el = document.createElement('div');
      el.id = INDICATOR_ID;
      el.className = INDICATOR_CLASS;
      document.body.appendChild(el);
    }
    el.textContent = message || DEFAULT_MESSAGE;
    el.classList.add(VISIBLE_CLASS);
    if (el._t) clearTimeout(el._t);
    el._t = setTimeout(function () { el.classList.remove(VISIBLE_CLASS); }, FADE_MS);
  }

  function readJSON(key) {
    try {
      var raw = localStorage.getItem(key);
      if (raw === null) return null;
      var parsed = JSON.parse(raw);
      return parsed === null ? null : parsed;
    } catch (e) {
      return null;
    }
  }

  function writeJSON(key, value) {
    try {
      localStorage.setItem(key, JSON.stringify(value));
      return true;
    } catch (e) {
      return false;
    }
  }

  function forKey(key) {
    return {
      key: key,
      load: function () {
        return readJSON(key);
      },
      save: function (data) {
        if (writeJSON(key, data)) showIndicator();
      },
      clear: function () {
        try { localStorage.removeItem(key); } catch (e) {}
      }
    };
  }

  function forSubkey(rootKey, subKey) {
    function readRoot() {
      var root = readJSON(rootKey);
      return (root && typeof root === 'object') ? root : {};
    }
    return {
      rootKey: rootKey,
      subKey: subKey,
      load: function () {
        var root = readRoot();
        var sub = root[subKey];
        return (sub === undefined) ? null : sub;
      },
      save: function (data) {
        var root = readRoot();
        root[subKey] = data;
        if (writeJSON(rootKey, root)) showIndicator();
      },
      clear: function () {
        var root = readRoot();
        if (Object.prototype.hasOwnProperty.call(root, subKey)) {
          delete root[subKey];
          writeJSON(rootKey, root);
        }
      }
    };
  }

  global.PlialuStorage = {
    forKey: forKey,
    forSubkey: forSubkey,
    showIndicator: showIndicator
  };
})(window);
